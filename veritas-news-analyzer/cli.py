#!/usr/bin/env python3
"""
Veritas News Analyzer - Command Line Interface
Використання: python cli.py [опції]
"""

import argparse
import sys
from pathlib import Path

# Додаємо app в path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from app.analyzer import NewsAnalyzer


def main():
    """Головна функція CLI"""
    
    parser = argparse.ArgumentParser(
        description='Veritas Protocol News Analyzer - Аналіз новин за логічною цілісністю',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:

  # Аналіз URL
  python cli.py --url https://www.bbc.com/news/article

  # Аналіз тексту
  python cli.py --text "Ваш текст тут"

  # Аналіз з файлу
  python cli.py --file article.txt

  # Перевірка репутації джерела
  python cli.py --reputation bbc.com

  # Експорт історії
  python cli.py --export history.json
        """
    )
    
    # Основні аргументи
    parser.add_argument('--url', '-u', 
                       help='URL новинної статті для аналізу')
    
    parser.add_argument('--text', '-t',
                       help='Текст для прямого аналізу')
    
    parser.add_argument('--file', '-f',
                       help='Файл з текстом для аналізу')
    
    parser.add_argument('--source', '-s',
                       default='Manual_Input',
                       help='Назва джерела (використовується з --text або --file)')
    
    parser.add_argument('--reputation', '-r',
                       help='Показати репутацію джерела')
    
    parser.add_argument('--export', '-e',
                       help='Експортувати історію аналізу в JSON файл')
    
    parser.add_argument('--json', '-j',
                       action='store_true',
                       help='Вивести результат у форматі JSON')
    
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Детальний вивід')
    
    args = parser.parse_args()
    
    # Перевірка аргументів
    if not any([args.url, args.text, args.file, args.reputation, args.export]):
        parser.print_help()
        sys.exit(1)
    
    # Ініціалізація аналізатора
    analyzer = NewsAnalyzer()
    
    # Обробка команд
    if args.reputation:
        # Показати репутацію джерела
        rep = analyzer.get_source_reputation(args.reputation)
        print(f"\n{'='*60}")
        print(f"Репутація джерела '{args.reputation}': {rep:.2f}")
        print(f"{'='*60}\n")
        return
    
    if args.export:
        # Експорт історії
        filename = analyzer.export_history(args.export)
        print(f"\n✅ Історію експортовано в: {filename}\n")
        return
    
    # Аналіз контенту
    result = None
    
    if args.url:
        # Аналіз URL
        if args.verbose:
            print(f"\n🔍 Аналізую URL: {args.url}\n")
        result = analyzer.analyze_url(args.url)
    
    elif args.file:
        # Аналіз з файлу
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
            if args.verbose:
                print(f"\n📄 Читаю файл: {args.file}\n")
            result = analyzer.analyze_text(text, args.source)
        except FileNotFoundError:
            print(f"\n❌ Помилка: Файл '{args.file}' не знайдено\n")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Помилка читання файлу: {e}\n")
            sys.exit(1)
    
    elif args.text:
        # Прямий аналіз тексту
        if args.verbose:
            print(f"\n📝 Аналізую текст від джерела: {args.source}\n")
        result = analyzer.analyze_text(args.text, args.source)
    
    # Вивід результату
    if result:
        if args.json:
            # JSON формат
            import json
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Звичайний формат
            print(analyzer.generate_report(result))
            print()


if __name__ == "__main__":
    main()
