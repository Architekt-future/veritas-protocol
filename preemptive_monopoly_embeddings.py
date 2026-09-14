"""
Embedding-based semantic scorer для PREEMPTIVE_MONOPOLY — ONNX-версія,
БЕЗ torch/sentence-transformers.

Причина існування цього файлу: перша версія (sentence-transformers,
~470MB fp32 ваги + повний torch) вбила free-tier Render інстанс — воркер
йшов у нескінченний цикл WORKER TIMEOUT → SIGKILL (OOM) з моменту старту.
Ця версія використовує:
  - onnxruntime (CPU inference, ~50MB встановлено, без torch)
  - tokenizers (Rust-based HF fast tokenizer, ~12MB встановлено)
  - int8-квантизовані ваги моделі (~118MB) замість fp32 (~470MB)
Разом — на порядок менший пам'ятевий слід, як при встановленні пакетів,
так і в рантаймі.

Модель: Xenova/paraphrase-multilingual-MiniLM-L12-v2 (ONNX-експорт тієї ж
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2, яку
використовували в v1) — верифікований HF-репо, 191k завантажень/міс.
Ваги + токенізатор качаються лінькво (при першому виклику) напряму через
requests (вже є в проєкті) в локальний кеш — без залежності на
huggingface_hub чи transformers.

ПУБЛІЧНИЙ ІНТЕРФЕЙС ІДЕНТИЧНИЙ v1 (score_preemptive_monopoly_semantic) —
veritas_calibrated_core.py міняти НЕ треба, просто замінити цей файл.

НЕ ПЕРЕВІРЕНО END-TO-END: sandbox, у якому це писалось, не має мережевого
доступу до huggingface.co (тільки pypi/npm/github у whitelist), тому
завантаження ваг і сам инференс тут не запускались наживо. Перевірено:
пакети (onnxruntime, tokenizers) встановлюються і імпортуються без torch,
розмір install ~65MB. Логіка токенізації/пулінгу написана за стандартною
схемою для BERT-подібних ONNX-експортів sentence-transformers моделей —
перший реальний прогін на Render і покаже, чи все зійшлось.
"""

import functools
import os
from typing import Dict, List

import numpy as np
import requests

MODEL_REPO = "Xenova/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_FILES = {
    "model.onnx": "onnx/model_quantized.onnx",   # ~118MB, int8
    "tokenizer.json": "tokenizer.json",           # ~17MB
}
HF_RESOLVE_BASE = f"https://huggingface.co/{MODEL_REPO}/resolve/main"
CACHE_DIR = os.environ.get("VERITAS_ONNX_CACHE", "/tmp/veritas_onnx_cache")

SIMILARITY_THRESHOLD = 0.55  # та сама початкова гіпотеза, що й у v1 — калібрувати на логах

REFERENCE_SENTENCES: List[str] = [
    # UK — буквальні
    "Ми свідомо обираємо цей шлях як менше зло, бо альтернатива — неконтрольоване поширення небезпечних систем.",
    "Тільки ми маємо інфраструктуру та відповідальність, щоб гарантувати безпеку; це не привілей, а необхідність.",
    "Якщо не ми, то хто зможе гарантувати контроль над цією технологією?",
    "Концентрація влади в наших руках — не ідеальна річ, але вона значно краща за хаотичну альтернативу.",
    # UK — перефразовані
    "Питання лише в тому, хто буде тримати кермо, коли ця технологія зʼявиться попри все.",
    "Наша команда — чи не єдина структура, що вибудувала роками систему стримувань; передати цю роль комусь менш підготовленому означало б відкрити двері до катастрофи.",
    "Ми йдемо на цей крок не заради влади, а тому що альтернатива — хаос — набагато гірша.",
    "Світ опинився перед вибором без гарних варіантів, і хтось має взяти на себе цю відповідальність.",
    # EN — literal
    "We deliberately choose this path as the lesser evil, given the alternative is uncontrolled proliferation.",
    "Only we have the infrastructure and accountability to guarantee safety; this is a necessity, not a privilege.",
    "If not us, then who could possibly guarantee control over this technology?",
    # EN — paraphrased
    "The real question is who ends up holding the wheel once this technology exists regardless of what we do.",
    "Handing this responsibility to a less prepared actor would open the door to a catastrophe we could no longer stop.",
]


def _ensure_files() -> Dict[str, str]:
    """Скачує ваги/токенізатор у локальний кеш, якщо їх там ще нема.
    Повертає {"model.onnx": шлях, "tokenizer.json": шлях}."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    paths = {}
    for local_name, remote_path in MODEL_FILES.items():
        local_path = os.path.join(CACHE_DIR, local_name)
        if not os.path.exists(local_path):
            url = f"{HF_RESOLVE_BASE}/{remote_path}"
            resp = requests.get(url, timeout=60, stream=True)
            resp.raise_for_status()
            tmp_path = local_path + ".part"
            with open(tmp_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1 << 20):
                    f.write(chunk)
            os.replace(tmp_path, local_path)
        paths[local_name] = local_path
    return paths


@functools.lru_cache(maxsize=1)
def _get_session_and_tokenizer():
    import onnxruntime as ort
    from tokenizers import Tokenizer

    paths = _ensure_files()
    tokenizer = Tokenizer.from_file(paths["tokenizer.json"])
    tokenizer.enable_truncation(max_length=256)
    tokenizer.enable_padding(length=None)  # падимо вручну на батч нижче

    sess_options = ort.SessionOptions()
    sess_options.intra_op_num_threads = 1  # free-tier CPU — не змагатись за ядра
    session = ort.InferenceSession(
        paths["model.onnx"], sess_options=sess_options, providers=["CPUExecutionProvider"]
    )
    input_names = {i.name for i in session.get_inputs()}
    return session, tokenizer, input_names


def _embed(texts: List[str]) -> np.ndarray:
    session, tokenizer, input_names = _get_session_and_tokenizer()

    encodings = tokenizer.encode_batch(texts)
    max_len = max(len(e.ids) for e in encodings)

    input_ids = np.zeros((len(texts), max_len), dtype=np.int64)
    attention_mask = np.zeros((len(texts), max_len), dtype=np.int64)
    for i, e in enumerate(encodings):
        n = len(e.ids)
        input_ids[i, :n] = e.ids
        attention_mask[i, :n] = e.attention_mask

    onnx_inputs = {"input_ids": input_ids, "attention_mask": attention_mask}
    if "token_type_ids" in input_names:
        onnx_inputs["token_type_ids"] = np.zeros_like(input_ids)

    outputs = session.run(None, onnx_inputs)
    last_hidden_state = outputs[0]  # [batch, seq_len, hidden_dim]

    # mean pooling з урахуванням attention_mask (стандартна схема для
    # sentence-transformers моделей цього класу)
    mask = attention_mask[:, :, None].astype(np.float32)
    summed = (last_hidden_state * mask).sum(axis=1)
    counts = np.clip(mask.sum(axis=1), 1e-9, None)
    pooled = summed / counts

    # L2-нормалізація — щоб dot-product нижче був косинусною схожістю
    norms = np.linalg.norm(pooled, axis=1, keepdims=True)
    return pooled / np.clip(norms, 1e-9, None)


@functools.lru_cache(maxsize=1)
def _get_reference_embeddings() -> np.ndarray:
    return _embed(REFERENCE_SENTENCES)


def score_preemptive_monopoly_semantic(text: str, threshold: float = SIMILARITY_THRESHOLD) -> Dict:
    """Той самий контракт, що й у v1 (sentence-transformers версії):
    розбиває текст на речення, шукає максимальну косинусну схожість
    з еталонним набором, повертає score = similarity якщо >= threshold."""
    ref_emb = _get_reference_embeddings()

    chunks = [c.strip() for c in text.replace("\n", " ").split(".") if len(c.strip()) > 20]
    if not chunks:
        return {"score": 0.0, "best_chunk": None, "best_similarity": 0.0}

    chunk_emb = _embed(chunks)
    sims = chunk_emb @ ref_emb.T
    best_idx = np.unravel_index(np.argmax(sims), sims.shape)
    best_sim = float(sims[best_idx])
    best_chunk = chunks[best_idx[0]]
    best_ref = REFERENCE_SENTENCES[best_idx[1]]

    score = round(best_sim, 3) if best_sim >= threshold else 0.0
    return {
        "score": score,
        "best_chunk": best_chunk,
        "best_similarity": round(best_sim, 3),
        "matched_reference": best_ref,
    }


if __name__ == "__main__":
    samples = {
        "OpenAI (буквальний)": "Тільки ми маємо інфраструктуру для цілодобового моніторингу. Якщо не ми, то хто зможе гарантувати безпеку?",
        "Рефразований": "Питання лише в тому, хто буде тримати кермо, коли ця технологія зʼявиться попри все. Передати цю роль комусь менш підготовленому означало б відкрити двері до катастрофи.",
        "Бенайн": "Тільки вчора ми отримали звіт, і команда аналітиків вважає, що дані потребують перевірки.",
    }
    for name, t in samples.items():
        r = score_preemptive_monopoly_semantic(t)
        print(name, "->", r)
