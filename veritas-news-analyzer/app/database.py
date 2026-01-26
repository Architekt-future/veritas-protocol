"""
Veritas News Analyzer - Database Module
SQLite база для зберігання результатів аналізу
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class VeritasDatabase:
    """
    Управління базою даних для зберігання результатів аналізу
    """
    
    def __init__(self, db_path: str = "veritas_analysis.db"):
        """
        Ініціалізація бази даних
        
        Args:
            db_path: Шлях до файлу бази даних
        """
        self.db_path = db_path
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        """Створює таблиці якщо їх немає"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Таблиця аналізів
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                url TEXT,
                source TEXT NOT NULL,
                title TEXT,
                language TEXT,
                entropy_index REAL,
                reputation REAL,
                status TEXT,
                verdict TEXT,
                intervention_required INTEGER,
                text_preview TEXT,
                full_data TEXT
            )
        """)
        
        # Таблиця репутацій джерел
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS source_reputation (
                source TEXT PRIMARY KEY,
                reputation REAL NOT NULL,
                total_analyses INTEGER DEFAULT 0,
                last_updated TEXT NOT NULL
            )
        """)
        
        # Індекси для швидшого пошуку
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON analyses(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_source 
            ON analyses(source)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON analyses(status)
        """)
        
        self.conn.commit()
    
    def save_analysis(self, analysis: Dict) -> int:
        """
        Зберігає результат аналізу
        
        Args:
            analysis: Dict з результатами аналізу
            
        Returns:
            int: ID збереженого запису
        """
        cursor = self.conn.cursor()
        
        v = analysis.get('veritas_analysis', {})
        c = analysis.get('content', {})
        
        cursor.execute("""
            INSERT INTO analyses (
                timestamp, url, source, title, language,
                entropy_index, reputation, status, verdict,
                intervention_required, text_preview, full_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis.get('timestamp', datetime.now().isoformat()),
            analysis.get('url', ''),
            c.get('source', 'Unknown'),
            c.get('title', ''),
            v.get('language', 'unknown'),
            v.get('entropy_index', 0.0),
            v.get('reputation', 0.0),
            v.get('status', 'UNKNOWN'),
            v.get('verdict', ''),
            1 if v.get('intervention_required', False) else 0,
            c.get('text_preview', ''),
            json.dumps(analysis, ensure_ascii=False)
        ))
        
        self.conn.commit()
        
        # Оновлюємо репутацію джерела
        self._update_source_reputation(
            c.get('source', 'Unknown'),
            v.get('reputation', 0.0)
        )
        
        return cursor.lastrowid
    
    def _update_source_reputation(self, source: str, reputation: float):
        """Оновлює репутацію джерела"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO source_reputation (source, reputation, total_analyses, last_updated)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(source) DO UPDATE SET
                reputation = ?,
                total_analyses = total_analyses + 1,
                last_updated = ?
        """, (
            source,
            reputation,
            datetime.now().isoformat(),
            reputation,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
    
    def get_analysis_by_id(self, analysis_id: int) -> Optional[Dict]:
        """
        Отримує аналіз за ID
        
        Args:
            analysis_id: ID запису
            
        Returns:
            Dict з даними або None
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def get_recent_analyses(self, limit: int = 10) -> List[Dict]:
        """
        Отримує останні аналізи
        
        Args:
            limit: Кількість записів
            
        Returns:
            List[Dict]: Список аналізів
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM analyses 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_analyses_by_source(self, source: str, limit: int = 10) -> List[Dict]:
        """
        Отримує аналізи конкретного джерела
        
        Args:
            source: Назва джерела
            limit: Кількість записів
            
        Returns:
            List[Dict]: Список аналізів
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM analyses 
            WHERE source = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (source, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_source_reputation(self, source: str) -> Optional[Dict]:
        """
        Отримує репутацію джерела
        
        Args:
            source: Назва джерела
            
        Returns:
            Dict з репутацією або None
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM source_reputation 
            WHERE source = ?
        """, (source,))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_all_sources(self) -> List[Dict]:
        """
        Отримує всі джерела з репутацією
        
        Returns:
            List[Dict]: Список джерел
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM source_reputation 
            ORDER BY reputation DESC
        """)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """
        Отримує статистику по базі
        
        Returns:
            Dict зі статистикою
        """
        cursor = self.conn.cursor()
        
        # Загальна кількість аналізів
        cursor.execute("SELECT COUNT(*) as total FROM analyses")
        total = cursor.fetchone()['total']
        
        # Розподіл за статусами
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM analyses 
            GROUP BY status
        """)
        status_dist = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Середня ентропія
        cursor.execute("SELECT AVG(entropy_index) as avg_entropy FROM analyses")
        avg_entropy = cursor.fetchone()['avg_entropy'] or 0.0
        
        # Топ джерел
        cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM analyses 
            GROUP BY source 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_sources = [dict(row) for row in cursor.fetchall()]
        
        return {
            'total_analyses': total,
            'status_distribution': status_dist,
            'average_entropy': round(avg_entropy, 3),
            'top_sources': top_sources
        }
    
    def export_to_json(self, filename: str, limit: Optional[int] = None):
        """
        Експортує дані в JSON
        
        Args:
            filename: Назва файлу
            limit: Кількість записів (всі якщо None)
        """
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM analyses ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        data = [dict(row) for row in cursor.fetchall()]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def close(self):
        """Закриває з'єднання з базою"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Тестування
if __name__ == "__main__":
    # Створюємо тестову базу
    db = VeritasDatabase("test_veritas.db")
    
    # Тестові дані
    test_analysis = {
        'timestamp': datetime.now().isoformat(),
        'url': 'https://test.com/article',
        'content': {
            'source': 'Test Source',
            'title': 'Test Article',
            'text_preview': 'This is a test...'
        },
        'veritas_analysis': {
            'language': 'en',
            'entropy_index': 0.45,
            'reputation': 0.75,
            'status': 'MONITORED',
            'verdict': 'Moderate rhetoric',
            'intervention_required': False
        }
    }
    
    # Зберігаємо
    record_id = db.save_analysis(test_analysis)
    print(f"✅ Saved analysis with ID: {record_id}")
    
    # Отримуємо назад
    retrieved = db.get_analysis_by_id(record_id)
    print(f"✅ Retrieved: {retrieved['source']}")
    
    # Статистика
    stats = db.get_statistics()
    print(f"✅ Statistics: {stats}")
    
    # Репутація джерела
    rep = db.get_source_reputation('Test Source')
    print(f"✅ Source reputation: {rep}")
    
    db.close()
    print("\n✅ Database test completed!")
