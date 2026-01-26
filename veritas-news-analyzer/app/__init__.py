"""
Veritas News Analyzer - Application Package
"""

__version__ = "1.0.0"
__author__ = "Architekt-future & Veritas Collective"

from .analyzer import NewsAnalyzer
from .scraper import NewsExtractor
from .translator import MultilingualVeritasCore, LanguageDetector

__all__ = [
    'NewsAnalyzer',
    'NewsExtractor', 
    'MultilingualVeritasCore',
    'LanguageDetector'
]
