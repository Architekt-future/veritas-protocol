# Veritas Protocol: Real-Time News Verifier
# Integrating Core Logic and Economy

from veritas_core import VeritasCore
from veritas_economy_proto import VeritasSecureEconomy

def run_verification():
    # Ініціалізація систем
    v_core = VeritasCore()
    v_econ = VeritasSecureEconomy()
    
    print("--- VERITAS PROTOCOL: VERIFIER MODE ---")
    entity_name = input("Enter Source Name (e.g., Lachen, FT, Reuters): ")
    news_text = input("Paste the news text to analyze: ")
    
    # 1. Аналіз ентропії через Core
    entropy_score = v_core.analyze_entropy(news_text)
    
    # 2. Економічний вердикт через Economy Module
    # (Передаємо текст в нашу економічну модель)
    result = v_econ.process_cycle(entity_name if entity_name in v_econ.registry else "Bot_Net_001", news_text)
    
    print("\n" + "="*40)
    print(f"ANALYSIS REPORT FOR: {entity_name}")
    print(f"Entropy Score: {entropy_score:.2f} (0=Logic, 1=Chaos)")
    print(f"Economic Impact: {result}")
    
    # Виводимо стан балансу після аналізу
    if entity_name in v_econ.registry:
        balance = v_econ.registry[entity_name]["balance"]
        trust = v_econ.registry[entity_name]["trust"]
        print(f"Updated Wallet: {balance:.2f} tokens | Trust Level: {trust:.2f}")
    print("="*40)

if __name__ == "__main__":
    # Для тесту можна запустити один цикл
    # Якщо хочеш перевіряти багато новин - додамо цикл while
    run_verification()
