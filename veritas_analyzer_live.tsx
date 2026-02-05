import React, { useState } from 'react';
import { AlertCircle, CheckCircle, XCircle, Info } from 'lucide-react';

const VeritasAnalyzer = () => {
  const [text, setText] = useState('');
  const [source, setSource] = useState('Manual Input');
  const [result, setResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  // Language detection
  const detectLanguage = (text) => {
    const ukrainianChars = /[їієґ]/;
    return ukrainianChars.test(text.toLowerCase()) ? 'uk' : 'en';
  };

  // Markers
  const markers = {
    uk: {
      noise: ['етично', 'необхідно', 'важливо', 'неприпустимо', 'історично', 
              'фундаментально', 'занепокоєння', 'перемога', 'збитки', 'довіра',
              'шокуюча', 'паніка', 'приховували', 'потрясла', 'сенсація', 'терміново'],
      signal: ['якщо', 'тоді', 'тому', 'внаслідок', 'дорівнює', 'факт',
               'ресурс', 'чип', 'наказ', 'координати', 'результат',
               'даних', 'показник', 'вимір', 'кількість', 'дослідження',
               'статистичний', 'кореляція', 'регресія', 'аналіз', 'респондентів'],
      chaos: ['рептилоїди', 'таємний', 'змова', 'плоска', 'контролюють',
              'масони', 'чіпування', 'підземелля', 'слонах']
    },
    en: {
      noise: ['ethically', 'necessarily', 'important', 'unacceptable', 'historically',
              'fundamentally', 'concern', 'victory', 'losses', 'trust',
              'shocking', 'panic', 'hidden', 'sensational', 'must', 'urgent'],
      signal: ['if', 'then', 'therefore', 'consequently', 'equals', 'fact',
               'resource', 'chip', 'order', 'coordinates', 'result',
               'data', 'metric', 'measurement', 'quantity', 'research',
               'statistical', 'correlation', 'regression', 'analysis', 'study',
               'rate', 'inflation', 'percentage', 'indicates', 'shows'],
      chaos: ['lizard', 'reptilian', 'magic', 'conspiracy', 'secret',
              'freemasons', 'microchip', 'underground', 'flat earth']
    }
  };

  const analyzeText = () => {
    setAnalyzing(true);
    
    setTimeout(() => {
      const lang = detectLanguage(text);
      const words = text.toLowerCase().replace(/[,\.]/g, '').split(/\s+/).filter(w => w.length > 0);
      
      if (words.length === 0) {
        setResult({ error: 'Будь ласка, введіть текст для аналізу' });
        setAnalyzing(false);
        return;
      }

      // Count numbers (Number Factor)
      const numberMatches = text.match(/\d+\.?\d*/g);
      const numberFactor = numberMatches ? numberMatches.length / (words.length + 1) : 0;

      // Count CAPS and exclamations (Shout Factor)
      const capsWords = text.split(/\s+/).filter(w => w === w.toUpperCase() && w.length > 2).length;
      const exclamations = (text.match(/!/g) || []).length;
      const questions = (text.match(/\?/g) || []).length;
      const shoutFactor = Math.min((exclamations * 2 + capsWords * 3 + questions) / (words.length + 1), 1.0);

      // Chaos markers (instant critical)
      const chaosCount = words.filter(w => 
        markers[lang].chaos.some(m => w.includes(m))
      ).length;

      if (chaosCount > 0) {
        setResult({
          source,
          language: lang.toUpperCase(),
          entropy: 0.99,
          status: 'CRITICAL',
          verdict: lang === 'uk' 
            ? 'КРИТИЧНА МАНІПУЛЯЦІЯ / ТОКСИЧНИЙ КОНТЕНТ'
            : 'CRITICAL MANIPULATION / TOXIC CONTENT',
          diagnostics: {
            numberFactor: numberFactor.toFixed(3),
            shoutFactor: shoutFactor.toFixed(3),
            chaosMarkers: chaosCount
          },
          details: {
            noise: 0,
            signal: 0,
            chaos: chaosCount
          }
        });
        setAnalyzing(false);
        return;
      }

      // Count noise and signal
      const noiseCount = words.filter(w => 
        markers[lang].noise.some(m => w.includes(m))
      ).length;
      
      const signalCount = words.filter(w => 
        markers[lang].signal.some(m => w.includes(m))
      ).length;

      // Base entropy
      const baseEntropy = (noiseCount + 1) / (signalCount + noiseCount + 1);

      // Final entropy with factors
      const finalEntropy = Math.min(
        baseEntropy * (1 - numberFactor * 0.3) + shoutFactor * 0.4,
        0.999
      );

      // Determine status
      let status, verdict;
      if (finalEntropy >= 0.7) {
        status = 'CRITICAL';
        verdict = lang === 'uk' 
          ? 'КРИТИЧНА МАНІПУЛЯЦІЯ / ТОКСИЧНИЙ КОНТЕНТ'
          : 'CRITICAL MANIPULATION / TOXIC CONTENT';
      } else if (finalEntropy >= 0.4) {
        status = 'WARNING';
        verdict = lang === 'uk'
          ? 'ПІДОЗРА НА РИТОРИЧНИЙ ШУМ'
          : 'SUSPECTED RHETORICAL NOISE';
      } else if (finalEntropy >= 0.2) {
        status = 'SUCCESS';
        verdict = lang === 'uk'
          ? 'ПРИЙНЯТНА ЯКІСТЬ ІНФОРМАЦІЇ'
          : 'ACCEPTABLE INFORMATION QUALITY';
      } else {
        status = 'TRUSTED';
        verdict = lang === 'uk'
          ? 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
          : 'STABLE LOGICAL SIGNAL';
      }

      setResult({
        source,
        language: lang.toUpperCase(),
        entropy: parseFloat(finalEntropy.toFixed(3)),
        status,
        verdict,
        diagnostics: {
          numberFactor: numberFactor.toFixed(3),
          shoutFactor: shoutFactor.toFixed(3),
          chaosMarkers: 0
        },
        details: {
          words: words.length,
          noise: noiseCount,
          signal: signalCount,
          chaos: 0
        }
      });
      
      setAnalyzing(false);
    }, 500);
  };

  const getStatusColor = (status) => {
    const colors = {
      'TRUSTED': 'bg-green-100 border-green-500 text-green-900',
      'SUCCESS': 'bg-green-50 border-green-400 text-green-800',
      'WARNING': 'bg-yellow-50 border-yellow-500 text-yellow-900',
      'CRITICAL': 'bg-red-100 border-red-500 text-red-900'
    };
    return colors[status] || 'bg-gray-100 border-gray-500';
  };

  const getStatusIcon = (status) => {
    if (status === 'TRUSTED' || status === 'SUCCESS') return <CheckCircle className="w-6 h-6" />;
    if (status === 'WARNING') return <AlertCircle className="w-6 h-6" />;
    return <XCircle className="w-6 h-6" />;
  };

  const examples = [
    {
      name: 'Scientific (Low Entropy)',
      text: 'У дослідженні взяли участь 2,847 респондентів віком від 18 до 65 років. Статистичний аналіз показав кореляцію 0.73 (p<0.01) між змінними A та B.',
      lang: 'uk'
    },
    {
      name: 'News (English)',
      text: 'The European Central Bank raised interest rates by 0.25 percentage points to 4.5%, marking the tenth consecutive increase.',
      lang: 'en'
    },
    {
      name: 'Political Rhetoric',
      text: 'Історично важливо зрозуміти, що необхідно діяти терміново! Етично неприпустимо ігнорувати цю критичну ситуацію!!!',
      lang: 'uk'
    },
    {
      name: 'Conspiracy (Critical)',
      text: 'Рептилоїди через масонську змову планують чіпування населення. Таємні сили контролюють все!!!',
      lang: 'uk'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            💠 Veritas Protocol
          </h1>
          <p className="text-gray-600 text-lg">
            Deterministic News Analyzer v2.0
          </p>
          <p className="text-sm text-gray-500 mt-2">
            "Truth is not an instrument. It is a witness."
          </p>
        </div>

        {/* Input Area */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Source Name
            </label>
            <input
              type="text"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="Enter source name..."
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Text to Analyze
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              rows="6"
              placeholder="Paste your text here for analysis..."
            />
          </div>

          <div className="flex gap-3">
            <button
              onClick={analyzeText}
              disabled={analyzing || !text.trim()}
              className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {analyzing ? 'Analyzing...' : '🔍 Analyze'}
            </button>
            <button
              onClick={() => { setText(''); setResult(null); }}
              className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all"
            >
              Clear
            </button>
          </div>

          {/* Examples */}
          <div className="mt-4">
            <p className="text-sm font-semibold text-gray-600 mb-2">Quick Examples:</p>
            <div className="flex flex-wrap gap-2">
              {examples.map((ex, idx) => (
                <button
                  key={idx}
                  onClick={() => setText(ex.text)}
                  className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-full transition-all"
                >
                  {ex.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Results */}
        {result && !result.error && (
          <div className={`rounded-lg shadow-lg p-6 border-l-4 ${getStatusColor(result.status)}`}>
            <div className="flex items-center gap-3 mb-4">
              {getStatusIcon(result.status)}
              <h2 className="text-2xl font-bold">Analysis Results</h2>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-white bg-opacity-50 rounded p-3">
                <p className="text-xs font-semibold text-gray-600">SOURCE</p>
                <p className="text-lg font-bold">{result.source}</p>
              </div>
              <div className="bg-white bg-opacity-50 rounded p-3">
                <p className="text-xs font-semibold text-gray-600">LANGUAGE</p>
                <p className="text-lg font-bold">{result.language}</p>
              </div>
              <div className="bg-white bg-opacity-50 rounded p-3">
                <p className="text-xs font-semibold text-gray-600">ENTROPY INDEX</p>
                <p className="text-lg font-bold">{result.entropy.toFixed(3)}</p>
              </div>
              <div className="bg-white bg-opacity-50 rounded p-3">
                <p className="text-xs font-semibold text-gray-600">STATUS</p>
                <p className="text-lg font-bold">{result.status}</p>
              </div>
            </div>

            <div className="bg-white bg-opacity-50 rounded p-4 mb-4">
              <p className="text-sm font-semibold text-gray-600 mb-1">VERDICT</p>
              <p className="text-lg font-bold">{result.verdict}</p>
            </div>

            {/* Diagnostics */}
            <div className="bg-white bg-opacity-50 rounded p-4">
              <p className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <Info className="w-4 h-4" />
                Diagnostics
              </p>
              <div className="grid grid-cols-3 gap-3 text-sm">
                <div>
                  <p className="text-gray-600">Number Factor</p>
                  <p className="font-bold">{result.diagnostics.numberFactor}</p>
                </div>
                <div>
                  <p className="text-gray-600">Shout Factor</p>
                  <p className="font-bold">{result.diagnostics.shoutFactor}</p>
                </div>
                <div>
                  <p className="text-gray-600">Chaos Markers</p>
                  <p className="font-bold">{result.diagnostics.chaosMarkers}</p>
                </div>
              </div>
              {result.details && (
                <div className="mt-3 pt-3 border-t border-gray-300">
                  <div className="grid grid-cols-3 gap-3 text-sm">
                    <div>
                      <p className="text-gray-600">Total Words</p>
                      <p className="font-bold">{result.details.words}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Noise Markers</p>
                      <p className="font-bold">{result.details.noise}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Signal Markers</p>
                      <p className="font-bold">{result.details.signal}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {result && result.error && (
          <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-4">
            <p className="text-red-800">{result.error}</p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-600">
          <p className="mb-2">
            <a href="https://github.com/Architekt-future/veritas-protocol" 
               target="_blank" 
               rel="noopener noreferrer"
               className="text-purple-600 hover:underline font-semibold">
              GitHub Repository
            </a>
            {' | '}
            <a href="https://osf.io/preprints/socarxiv/9pbaj" 
               target="_blank" 
               rel="noopener noreferrer"
               className="text-purple-600 hover:underline font-semibold">
              Academic Paper
            </a>
          </p>
          <p className="text-xs text-gray-500">
            Veritas Protocol v2.0 | Co-authored by Dmytro Kholodniak, Claude, ChatGPT, Gemini
          </p>
        </div>
      </div>
    </div>
  );
};

export default VeritasAnalyzer;