import csv
from datetime import datetime
from veritas_core import VeritasCore
from veritas_economy_proto import VeritasSecureEconomy

def log_to_csv(entity, score, result):
    # Функція запису результату в файл audit_log.csv
    file_exists = False
    try:
        with open('audit_log.csv', 'r') as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open('audit_log.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Якщо файл новий - додаємо заголовки
        if not file_exists:
            writer.writerow(['Timestamp', 'Source', 'Entropy_Score', 'Economic_Verdict'])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            entity,
            f"{score:.2f}",
            result
        ])

def run_verification():
    v_core = VeritasCore()
    v_econ = VeritasSecureEconomy()
    
    print("\n--- VERITAS PROTOCOL: VERIFIER MODE ---")
    entity_name = input("Enter Source Name (e.g., Lachen, FT, Reuters): ")
    news_text = input("Paste the news text to analyze: ")
    
    # 1. Аналіз
    entropy_score = v_core.analyze_entropy(news_text)
    result = v_econ.process_cycle(entity_name if entity_name in v_econ.registry else "Bot_Net_001", news_text)
    
    # 2. Логування в CSV
    log_to_csv(entity_name, entropy_score, result)
    
    print("\n" + "="*40)
    print(f"ANALYSIS REPORT FOR: {entity_name}")
    print(f"Entropy Score: {entropy_score:.2f} (0=Logic, 1=Chaos)")
    print(f"Economic Impact: {result}")
    print(f"Status: Result saved to audit_log.csv")
    print("="*40)

if __name__ == "__main__":
    run_verification()
