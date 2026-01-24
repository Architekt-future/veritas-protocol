import os
from core import VeritasCore
from states import get_action_protocol

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_gauge(value, length=20):
    """Малює візуальну шкалу ентропії"""
    filled = int(value * length)
    bar = "█" * filled + "-" * (length - filled)
    return f"[{bar}] {value*100:.1f}%"

def run_interface():
    core = VeritasCore()
    
    while True:
        clear_screen()
        print("="*50)
        print("   VERITAS PROTOCOL v7.2 - МОНІТОР ІСТИНИ")
        print("="*50)
        print("\n[ДОСТУПНІ ВУЗЛИ]:", ", ".join(core.reputation_registry.keys()))
        
        print("\n" + "-"*50)
        source = input("Введіть назву джерела (або 'exit'): ").strip()
        if source.lower() == 'exit': break
        
        text = input("Введіть текст для аналізу: ").strip()
        if not text: continue

        # Виконання аналізу
        result = core.evaluate_integrity(text, source)
        state = core.get_system_state(source)
        action = get_action_protocol(state)

        # Вивід результатів (Мінімалізм)
        clear_screen()
        print("="*50)
        print(f"ДЖЕРЕЛО: {source}")
        print(f"СТАН:    {state.name}")
        print(f"ЕНТРОПІЯ: {draw_gauge(result['entropy_index'])}")
        print(f"РЕПУТАЦІЯ: {result['new_reputation']}")
        print("-"*50)
        print(f"ПРОТОКОЛ ДІЇ: {action}")
        print("-"*50)
        
        input("\nНатисніть Enter, щоб продовжити...")

if __name__ == "__main__":
    run_interface()
