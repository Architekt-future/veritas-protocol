import re

def verify_news(text):
    # Початковий бал стабільності (Entropy Stability Index)
    esi_score = 1.0  
    warnings = []

    print("\n" + "="*40)
    print("   VERITAS PROTOCOL: LOGIC CHECK")
    print("="*40)

    # 1. SMART INSTITUTIONAL FILTER (Твоє залізне правило)
    # Шукаємо абревіатури (2+ великі літери) або слова з великої літери (власні назви)
    org_pattern = r'\b[А-ЯA-Z]{2,}\b'
    mentions_org = re.findall(org_pattern, text)
    
    # Якщо є організації, але немає жодного посилання (http/https)
    has_link = re.search(r'https?://', text)
    if mentions_org and not has_link:
        penalty = 0.4
        esi_score -= penalty
        unique_orgs = ", ".join(set(mentions_org[:5])) # показуємо перші 5 для звіту
        warnings.append(f"БАМ! Згадуються структури ({unique_orgs}) без лінку на джерело (-{penalty} ESI)")

    # 2. CAPS LOCK FILTER (Детектор ентропії та емоційного тиску)
    # Якщо більше 20% тексту написано капсом (крім коротких абревіатур)
    caps_words = re.findall(r'\b[А-ЯA-Z]{4,}\b', text)
    if len(caps_words) > 3: # Якщо більше 3 довгих слів капсом
        penalty = 0.2
        esi_score -= penalty
        warnings.append(f"Виявлено надлишковий CAPS LOCK. Ознака маніпуляції (-{penalty} ESI)")

    # 3. HYPE KEYWORDS (Словник маніпулятора)
    hype_words = [
        "історичний", "визначний", "вперше", "похвалилася", 
        "вдалий крок", "шок", "терміново", "сенсація"
    ]
    found_hype = [w for w in hype_words if w.lower() in text.lower()]
    if found_hype:
        penalty = 0.1 * len(found_hype)
        esi_score -= penalty
        warnings.append(f"Емоційні маркери: {', '.join(found_hype)} (-{round(penalty, 1)} ESI)")

    # 4. ПЕРЕВІРКА НА ПОРОЖНІЙ ТЕКСТ АБО ОДИН ПРЯМИЙ ЛІНК
    if len(text.strip()) < 10:
        return "Помилка: Недостатньо даних для аналізу."

    # Фінальний розрахунок (не нижче 0)
    esi_score = max(0.0, round(esi_score, 2))
    
    # ВИВІД РЕЗУЛЬТАТІВ
    print(f"АНАЛІЗ: {text[:100]}...")
    print(f"\nESI INDEX: {esi_score} / 1.0")
    
    if esi_score >= 0.8:
        status = "✅ STABLE (Висока довіра)"
    elif 0.5 <= esi_score < 0.8:
        status = "⚠️ SUSPICIOUS (Середня ентропія / Потребує верифікації)"
    else:
        status = "❌ UNSTABLE (Висока ентропія / Ознаки фейку)"
    
    print(f"СТАТУС: {status}")

    if warnings:
        print("\nВИЯВЛЕНІ АНОМАЛІЇ:")
        for w in warnings:
            print(f"  [!] {w}")
    
    print("="*40)

# Запуск
if __name__ == "__main__":
    print("Veritas Protocol v1.2-alpha завантажено.")
    user_input = input("Вставте текст для перевірки: ")
    verify_news(user_input)
