"""
Veritas News Analyzer - Main Analysis Module
Об'єднує scraping, аналіз та звітність
"""

from typing import Dict, List
import json
from datetime import datetime
import logging

# Імпорт наших модулів
try:
    from .scraper import NewsExtractor
    from .translator import MultilingualVeritasCore
except ImportError:
    # Для standalone запуску
    import sys
    sys.path.append('.')
    from scraper import NewsExtractor
    from translator import MultilingualVeritasCore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsAnalyzer:
    """
    Головний аналізатор новин за Veritas Protocol
    """
    
    def __init__(self, config: Dict = None):
        self.extractor = NewsExtractor()
        self.veritas = MultilingualVeritasCore(config=config)
        self.analysis_history: List[Dict] = []
        self.config = config or {}
    
    def analyze_url(self, url: str, save_history: bool = True) -> Dict:
        """
        Повний аналіз новини з URL
        
        Args:
            url: URL новинної статті
            save_history: Чи зберігати в історію
            
        Returns:
            Dict з повним аналізом
        """
        logger.info(f"Starting analysis of: {url}")
        
        # 1. Витягуємо контент
        content = self.extractor.extract_from_url(url)
        
        if not content['success']:
            return {
                'success': False,
                'error': content['error'],
                'url': url,
                'timestamp': datetime.now().isoformat()
            }
        
        # 2. Аналізуємо за Veritas Protocol
        analysis = self.veritas.evaluate_integrity(
            text=content['text'],
            source=content['source']
        )
        
        # 3. Формуємо повний звіт
        full_report = {
            'success': True,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'content': {
                'title': content['title'],
                'source': content['source'],
                'text_length': len(content['text']),
                'text_preview': content['text'][:500] + '...' if len(content['text']) > 500 else content['text']
            },
            'veritas_analysis': {
                'language': analysis['language'],
                'entropy_index': analysis['entropy_index'],
                'reputation': analysis['reputation'],
                'status': analysis['status'],
                'verdict': analysis['verdict'],
                'intervention_required': analysis['intervention_required']
            },
            'recommendation': self._get_recommendation(analysis)
        }
        
        # 4. Зберігаємо в історію
        if save_history:
            self.analysis_history.append(full_report)
        
        logger.info(f"Analysis complete: {analysis['status']}")
        return full_report
    
    def analyze_text(self, text: str, source: str = "Manual_Input") -> Dict:
        """
        Аналіз тексту без витягування з URL
        
        Args:
            text: Текст для аналізу
            source: Назва джерела
            
        Returns:
            Dict з аналізом
        """
        analysis = self.veritas.evaluate_integrity(text=text, source=source)
        
        return {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'content': {
                'source': source,
                'text_length': len(text),
                'text_preview': text[:500] + '...' if len(text) > 500 else text
            },
            'veritas_analysis': analysis,
            'recommendation': self._get_recommendation(analysis)
        }
    
    def _get_recommendation(self, analysis: Dict) -> Dict:
        """
        Генерує рекомендації на основі аналізу
        """
        entropy = analysis['entropy_index']
        status = analysis['status']
        language = analysis['language']
        
        recommendations = {
            'uk': {
                'TRUSTED': "✅ Джерело можна вважати надійним",
                'MONITORED': "⚠️ Рекомендується перевірка фактів",
                'WARNING': "🔶 Високий рівень риторики. Критичний аналіз обов'язковий",
                'REJECTED': "❌ Джерело не рекомендується як основне"
            },
            'en': {
                'TRUSTED': "✅ Source can be considered reliable",
                'MONITORED': "⚠️ Fact-checking recommended",
                'WARNING': "🔶 High level of rhetoric. Critical analysis required",
                'REJECTED': "❌ Source not recommended as primary"
            }
        }
        
        details = {
            'uk': {
                'action': 'Використовувати' if status in ['TRUSTED', 'MONITORED'] else 'Уникати',
                'trust_level': self._map_trust_level(entropy, 'uk'),
                'critical_thinking': 'Низький' if entropy < 0.3 else 'Високий'
            },
            'en': {
                'action': 'Use' if status in ['TRUSTED', 'MONITORED'] else 'Avoid',
                'trust_level': self._map_trust_level(entropy, 'en'),
                'critical_thinking': 'Low' if entropy < 0.3 else 'High'
            }
        }
        
        return {
            'message': recommendations[language][status],
            'action': details[language]['action'],
            'trust_level': details[language]['trust_level'],
            'critical_thinking_required': details[language]['critical_thinking']
        }
    
    def _map_trust_level(self, entropy: float, language: str) -> str:
        """Мапить entropy на рівень довіри"""
        levels = {
            'uk': ['Дуже високий', 'Високий', 'Середній', 'Низький', 'Дуже низький'],
            'en': ['Very High', 'High', 'Medium', 'Low', 'Very Low']
        }
        
        if entropy < 0.2:
            return levels[language][0]
        elif entropy < 0.4:
            return levels[language][1]
        elif entropy < 0.6:
            return levels[language][2]
        elif entropy < 0.8:
            return levels[language][3]
        else:
            return levels[language][4]
    
    def get_source_reputation(self, source: str) -> float:
        """Повертає поточну репутацію джерела"""
        return self.veritas.reputation_registry.get(source, 0.5)
    
    def export_history(self, filename: str = None) -> str:
        """
        Експортує історію аналізу в JSON
        
        Args:
            filename: Назва файлу (опціонально)
            
        Returns:
            Шлях до збереженого файлу
        """
        if filename is None:
            filename = f"veritas_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_history, f, ensure_ascii=False, indent=2)
        
        logger.info(f"History exported to: {filename}")
        return filename
    
    def generate_report(self, analysis: Dict) -> str:
        """
        Генерує текстовий звіт
        
        Args:
            analysis: Результат аналізу
            
        Returns:
            Форматований текстовий звіт
        """
        if not analysis['success']:
            return f"❌ Error analyzing URL: {analysis.get('error', 'Unknown error')}"
        
        v = analysis['veritas_analysis']
        c = analysis['content']
        r = analysis['recommendation']
        
        lang = v['language']
        
        if lang == 'uk':
            report = f"""
╔═══════════════════════════════════════════════════════════════╗
║           VERITAS PROTOCOL - АНАЛІЗ НОВИНИ                    ║
╚═══════════════════════════════════════════════════════════════╝

📰 ЗАГОЛОВОК: {c['title']}
🌐 ДЖЕРЕЛО: {c['source']}
🔗 URL: {analysis['url']}
📅 ЧАС АНАЛІЗУ: {analysis['timestamp']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 АНАЛІЗ VERITAS PROTOCOL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Індекс ентропії: {v['entropy_index']:.3f}
📈 Репутація джерела: {v['reputation']:.2f}
🏷️  Статус: {v['status']}
💬 Вердикт: {v['verdict']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 РЕКОМЕНДАЦІЇ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{r['message']}

✓ Дія: {r['action']}
✓ Рівень довіри: {r['trust_level']}
✓ Критичне мислення: {r['critical_thinking_required']}

{'⚠️  ПОТРІБНЕ ВТРУЧАННЯ!' if v['intervention_required'] else ''}
            """
        else:  # English
            report = f"""
╔═══════════════════════════════════════════════════════════════╗
║           VERITAS PROTOCOL - NEWS ANALYSIS                    ║
╚═══════════════════════════════════════════════════════════════╝

📰 TITLE: {c['title']}
🌐 SOURCE: {c['source']}
🔗 URL: {analysis['url']}
📅 ANALYSIS TIME: {analysis['timestamp']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 VERITAS PROTOCOL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Entropy Index: {v['entropy_index']:.3f}
📈 Source Reputation: {v['reputation']:.2f}
🏷️  Status: {v['status']}
💬 Verdict: {v['verdict']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{r['message']}

✓ Action: {r['action']}
✓ Trust Level: {r['trust_level']}
✓ Critical Thinking Required: {r['critical_thinking_required']}

{'⚠️  INTERVENTION REQUIRED!' if v['intervention_required'] else ''}
            """
        
        return report.strip()


# Тестування
if __name__ == "__main__":
    analyzer = NewsAnalyzer()
    
    # Приклад 1: Аналіз тексту українською
    print("\n" + "="*70)
    print("TEST 1: Ukrainian Text Analysis")
    print("="*70)
    
    uk_text = "Історично важливо етично занепокоїтися через фундаментальну втрату довіри до інститутів."
    result1 = analyzer.analyze_text(uk_text, "TestSource_UA")
    print(analyzer.generate_report(result1))
    
    # Приклад 2: Аналіз тексту англійською
    print("\n" + "="*70)
    print("TEST 2: English Text Analysis")
    print("="*70)
    
    en_text = "If the data equals zero, then the result consequently indicates a measurement error."
    result2 = analyzer.analyze_text(en_text, "TestSource_EN")
    print(analyzer.generate_report(result2))
    
    # Приклад 3: Аналіз URL (закоментовано, бо потрібен реальний URL)
    # print("\n" + "="*70)
    # print("TEST 3: URL Analysis")
    # print("="*70)
    # url = "https://www.bbc.com/news/world"
    # result3 = analyzer.analyze_url(url)
    # print(analyzer.generate_report(result3))
