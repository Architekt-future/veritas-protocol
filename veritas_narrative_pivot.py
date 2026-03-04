"""
Veritas Narrative Pivot Detector v1.0
Detects when a text starts with one topic and ends with another —
a classic tabloid/propaganda technique to smuggle conclusions.

Examples:
  - UFO server wipe → JFK → Epstein → Trump
  - Sports story → political message at the end
  - Science article → conspiracy conclusion
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional
from collections import Counter


@dataclass
class PivotResult:
    has_pivot:      bool
    score:          float          # 0.0 - 1.0
    verdict:        str
    start_topics:   List[str]
    end_topics:     List[str]
    pivot_point:    Optional[int]  # paragraph index where pivot occurs
    explanation:    str
    evidence:       List[str] = field(default_factory=list)


class NarrativePivotDetector:

    # Topic clusters — words that belong to the same semantic field
    TOPIC_CLUSTERS = {
        'технологія':   [r'\b(сервер|файл|архів|дан[іа]|хакер|кіберат|програм|сайт|бекап|хостинг)\b',
                         r'\b(server|file|data|hack|cyber|software|backup|hosting|deleted|wiped)\b'],
        'нло_космос':   [r'\b(нло|уфо|прибулець|позаземн|розвелл|uap|ufo|alien|extraterr|roswell|spacecraft)\b',
                         r'\b(маєстік|majestic|cia.ufo|pentagon.ufo)\b'],
        'змова':        [r'\b(змов|конспір|приховат|таємн|розсекречен|conspiracy|cover.up|secret|classified|deep.state)\b'],
        'політика':     [r'\b(трамп|байден|обама|конгрес|сенат|trump|biden|obama|congress|senate|president|адмін)\b'],
        'епштейн':      [r'\b(епштейн|epstein)\b',
                         r'\b(jeffrey\s+epstein|джеффрі\s+епштейн)\b'],
        'кеннеді':      [r'\b(кеннеді|kennedy|jfk|вбивств)\b'],
        'cia_fbi':      [r'\b(cia|фбр|fbi)\b',
                         r'\b(spy\s+agenc|secret\s+service|deep\s+state)\b',
                         r'\b(розвідувальн[аеі]\s+агенц|спецслужб)\b'],
        'військо':      [r'\b(пентагон|pentagon|dod)\b',
                         r'\b(military\s+(base|operation|force|budget|action|command))\b',
                         r'\b(armed\s+forces|department\s+of\s+defense)\b',
                         r'\b(армі|військ).{1,20}(операц|бюджет|сил|бази|командуванн)\b'],
        'економіка':    [r'\b(інвестиц|ринок|акці|дохід|invest|market|stock|revenue|profit)\b'],
        'здоров':       [r'\b(лікар|хвороб|вакцин|doctor|vaccine|health|медицин)\b'],
    }

    PIVOT_CONNECTORS = [
        r'\bтакож варто згадати\b',
        r'\bкрім того\b.*\b(епштейн|кеннеді|трамп|змов)\b',
        r'\bбагато хто в соцмережах\b',
        r'\bcritics.+claim\b',
        r'\bmany on social media\b',
        r'\bsome have pointed (out|to)\b',
        r'\bit is worth noting\b',
        r'\bthis comes as\b',
        r'\bin related news\b',
        r'\bmeaning while\b',
    ]

    def analyze(self, text: str) -> PivotResult:
        # Try double newlines first, fall back to single newlines, then sentence splitting
        paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if len(p.strip()) > 30]
        if len(paragraphs) < 4:
            paragraphs = [p.strip() for p in re.split(r'\n', text) if len(p.strip()) > 30]
        if len(paragraphs) < 4:
            # Split by sentences — every 3 sentences = 1 "paragraph"
            sentences = re.split(r'(?<=[.!?])\s+', text)
            paragraphs = []
            for i in range(0, len(sentences), 3):
                chunk = ' '.join(sentences[i:i+3]).strip()
                if len(chunk) > 30:
                    paragraphs.append(chunk)

        if len(paragraphs) < 3:
            return PivotResult(
                has_pivot=False, score=0.0,
                verdict='INSUFFICIENT_TEXT',
                start_topics=[], end_topics=[],
                pivot_point=None,
                explanation='Недостатньо тексту для аналізу структури наративу.'
            )

        # Split into thirds
        third = max(1, len(paragraphs) // 3)
        start_paras = paragraphs[:third]
        end_paras   = paragraphs[-third:]

        start_topics = self._detect_topics(' '.join(start_paras))
        end_topics   = self._detect_topics(' '.join(end_paras))

        # Find pivot connectors
        pivot_evidence = []
        pivot_point = None
        for i, para in enumerate(paragraphs):
            for pattern in self.PIVOT_CONNECTORS:
                if re.search(pattern, para, re.IGNORECASE):
                    pivot_evidence.append(para[:120])
                    if pivot_point is None:
                        pivot_point = i
                    break

        # Calculate topic divergence
        start_set = set(start_topics)
        end_set   = set(end_topics)
        shared    = start_set & end_set
        diverged  = end_set - start_set

        if not start_set:
            divergence = 0.0
        else:
            divergence = len(diverged) / max(len(start_set | end_set), 1)

        # Boost score for known dangerous pivots
        dangerous_end_topics = {'епштейн', 'кеннеді', 'змова', 'epstein', 'kennedy', 'conspiracy'}
        danger_boost = 0.3 if any(t in dangerous_end_topics for t in end_set - start_set) else 0.0

        # Boost for pivot connectors
        connector_boost = min(0.2 * len(pivot_evidence), 0.3)

        score = min(divergence + danger_boost + connector_boost, 1.0)
        has_pivot = score >= 0.35

        # Build verdict
        if score >= 0.7:
            verdict = 'STRONG_PIVOT'
        elif score >= 0.45:
            verdict = 'MODERATE_PIVOT'
        elif score >= 0.35:
            verdict = 'WEAK_PIVOT'
        else:
            verdict = 'NO_PIVOT'

        # Build explanation
        if has_pivot:
            start_str = ', '.join(start_topics[:3]) or 'невизначено'
            end_str   = ', '.join(end_topics[:3]) or 'невизначено'
            explanation = (
                f'Текст починається з теми "{start_str}" але закінчується темою "{end_str}". '
                f'Такий перехід може бути навмисним — щоб непомітно підвести читача до висновку '
                f'який не випливає з початкової теми.'
            )
        else:
            explanation = 'Наратив тексту розвивається послідовно без різких тематичних стрибків.'

        return PivotResult(
            has_pivot=has_pivot,
            score=round(score, 3),
            verdict=verdict,
            start_topics=start_topics,
            end_topics=end_topics,
            pivot_point=pivot_point,
            explanation=explanation,
            evidence=pivot_evidence[:3],
        )

    # Topics that require 2+ pattern hits to avoid single-word false positives
    HIGH_THRESHOLD_TOPICS = {'cia_fbi', 'змова', 'нло_космос'}

    def _detect_topics(self, text: str) -> List[str]:
        found = []
        t = text.lower()
        for topic, patterns in self.TOPIC_CLUSTERS.items():
            hits = sum(1 for p in patterns if re.search(p, t, re.IGNORECASE))
            min_hits = 2 if topic in self.HIGH_THRESHOLD_TOPICS else 1
            if hits >= min_hits:
                found.append(topic)
        return found


if __name__ == '__main__':
    d = NarrativePivotDetector()

    daily_mail = """A massive public archive of declassified US government files vanished just one day after President Trump ordered the release of all UFO-related documents.

The Black Vault, run by researcher and ufologist John Greenewald Jr, had its main server reportedly wiped clean on February 20, deleting hundreds of gigabytes worth of files on UFOs, declassified CIA projects, and major conspiracies, including the assassination of JFK.

Greenewald shared the news online, explaining that some server directories had their permissions changed without explanation.

Black Vault has become a go-to resource for anyone wanting to see exactly what the government has quietly made public over the last 80 years.

Greenewald has spent three decades organizing information on hidden programs and little-known incidents that suggest the US has been involved in top secret efforts to recover and take advantage of alien technology.

Troves of declassified files the public can freely search through on the Black Vault detail military base reports, witness testimonies, and even CIA directives since the 1940s and 50s.

The timing of the potential sabotage came just hours after the president's history-making declaration, ordering the Pentagon to disclose anything related to alien and extraterrestrial life.

Data wipes like this can occur in a few ways, often without it being a malicious attack.

Many on social media have pointed to the previous releases of the documents detailing President Kennedy assassination and the Jeffrey Epstein files both containing heavily redacted information that provided no definitive smoking gun."""

    r = d.analyze(daily_mail)
    print(f'has_pivot: {r.has_pivot}')
    print(f'score: {r.score}')
    print(f'verdict: {r.verdict}')
    print(f'start_topics: {r.start_topics}')
    print(f'end_topics: {r.end_topics}')
    print(f'pivot_point: paragraph {r.pivot_point}')
    print(f'explanation: {r.explanation}')
    print(f'evidence: {r.evidence}')
