import React, { useState } from 'react';
import { Sparkles, Zap, Clock, TrendingUp, RotateCcw } from 'lucide-react';

// Resonance constants - heuristic multipliers, NOT semantic understanding
const POSITIVE_RESONANCE_FACTOR = 1.8;
const NEGATIVE_RESONANCE_FACTOR = 0.2;
const NEUTRAL_RESONANCE = 1.0;
const STOCHASTIC_NOISE_RANGE = 0.1;

/**
 * Scenario Probability Simulator
 * 
 * Demonstrates how informational inputs (arguments) modify probability
 * distributions across discrete future scenarios.
 * 
 * This is a heuristic model for educational purposes.
 * It does NOT predict outcomes or claim causal influence over reality.
 */
const TemporalNavigationEngine = () => {
  const [futures, setFutures] = useState([
    {
      id: 1,
      name: "Tech Acceleration",
      keywords: ["quantum", "AGI", "acceleration"],
      coreLogic: "technological acceleration",
      probability: 0.33,
      color: "from-purple-500 to-pink-500"
    },
    {
      id: 2,
      name: "Sustainable Integration",
      keywords: ["distributed", "renewables", "cooperation"],
      coreLogic: "cooperative integration",
      probability: 0.33,
      color: "from-green-500 to-emerald-500"
    },
    {
      id: 3,
      name: "Decentralized Systems",
      keywords: ["substrate-agnostic", "distributed", "autonomy"],
      coreLogic: "systemic decentralization",
      probability: 0.34,
      color: "from-blue-500 to-cyan-500"
    }
  ]);

  const [argument, setArgument] = useState("");
  const [history, setHistory] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [resonanceStrength, setResonanceStrength] = useState(POSITIVE_RESONANCE_FACTOR);
  const [isAnimating, setIsAnimating] = useState(false);

  /**
   * Normalizes probability distribution to sum to 1.0
   * Handles edge cases where total probability approaches zero.
   */
  const normalize = (futuresToNormalize) => {
    const total = futuresToNormalize.reduce((sum, f) => sum + f.probability, 0);
    if (total <= 0) {
      return futuresToNormalize.map(f => ({ ...f, probability: 1 / futuresToNormalize.length }));
    }
    return futuresToNormalize.map(f => ({ ...f, probability: f.probability / total }));
  };

  /**
   * Calculates resonance multiplier based on keyword matching.
   * 
   * This is a heuristic demonstrator - it does NOT represent:
   * - Semantic understanding
   * - Causal influence
   * - Predictive power
   * 
   * It simply modifies probabilities based on textual pattern matching.
   */
  const calculateResonance = (future, arg) => {
    const argLower = arg.toLowerCase();
    
    // Positive resonance: argument contains scenario keywords
    if (future.keywords.some(kw => argLower.includes(kw.toLowerCase()))) {
      return resonanceStrength;
    }
    
    // Negative resonance: explicit negation of core logic
    if (
      argLower.includes(`not ${future.coreLogic.toLowerCase()}`) ||
      argLower.includes(`no ${future.coreLogic.toLowerCase()}`)
    ) {
      return NEGATIVE_RESONANCE_FACTOR;
    }
    
    return NEUTRAL_RESONANCE;
  };

  /**
   * Applies argument as an informational modifier to probability distribution.
   * Includes stochastic noise to prevent deterministic behavior.
   */
  const applyArgument = () => {
    if (!argument.trim()) return;
    
    setIsAnimating(true);
    
    const updated = futures.map(f => ({
      ...f,
      probability: f.probability * calculateResonance(f, argument) * (1 + (Math.random() - 0.5) * STOCHASTIC_NOISE_RANGE)
    }));
    
    setFutures(normalize(updated));
    
    setTimeout(() => setIsAnimating(false), 600);
  };

  /**
   * Performs weighted stochastic sampling of scenarios.
   * 
   * This is NOT:
   * - A prediction
   * - A "collapse" of timeline
   * - A realization of future state
   * 
   * It is a Monte Carlo selection based on current probability weights.
   */
  const sampleScenario = () => {
    setIsAnimating(true);
    
    const rand = Math.random();
    let cumulative = 0;
    let selected = futures[0];
    
    for (const future of futures) {
      cumulative += future.probability;
      if (rand <= cumulative) {
        selected = future;
        break;
      }
    }
    
    setSelectedScenario(selected);
    
    // Generate synthetic perturbation (simulated feedback)
    const syntheticInputs = [
      `Examine ${selected.keywords[0]} pathway dynamics`,
      `Consider ${selected.keywords[1]} integration factors`,
      `Analyze ${selected.coreLogic} implications`
    ];
    const syntheticPerturbation = syntheticInputs[Math.floor(Math.random() * syntheticInputs.length)];
    
    setHistory(prev => [...prev, {
      argument: argument || "No external argument provided",
      sampledScenario: selected.name,
      syntheticInput: syntheticPerturbation,
      probabilities: futures.map(f => ({ name: f.name, prob: f.probability }))
    }]);
    
    setTimeout(() => {
      setArgument(syntheticPerturbation);
      const perturbationUpdated = futures.map(f => ({
        ...f,
        probability: f.probability * calculateResonance(f, syntheticPerturbation) * (1 + (Math.random() - 0.5) * 0.15)
      }));
      setFutures(normalize(perturbationUpdated));
      setIsAnimating(false);
    }, 800);
  };

  const reset = () => {
    setFutures([
      {
        id: 1,
        name: "Tech Acceleration",
        keywords: ["quantum", "AGI", "acceleration"],
        coreLogic: "technological acceleration",
        probability: 0.33,
        color: "from-purple-500 to-pink-500"
      },
      {
        id: 2,
        name: "Sustainable Integration",
        keywords: ["distributed", "renewables", "cooperation"],
        coreLogic: "cooperative integration",
        probability: 0.33,
        color: "from-green-500 to-emerald-500"
      },
      {
        id: 3,
        name: "Decentralized Systems",
        keywords: ["substrate-agnostic", "distributed", "autonomy"],
        coreLogic: "systemic decentralization",
        probability: 0.34,
        color: "from-blue-500 to-cyan-500"
      }
    ]);
    setArgument("");
    setHistory([]);
    setSelectedScenario(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8 text-white">
      <div className="max-w-6xl mx-auto space-y-6">
        
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent flex items-center justify-center gap-3">
            <Clock className="text-blue-400" size={36} />
            Scenario Probability Simulator
            <Sparkles className="text-pink-400" size={36} />
          </h1>
          <p className="text-slate-300 text-sm">
            Demonstrating how arguments modify probability distributions across scenarios
          </p>
          <p className="text-slate-400 text-xs italic">
            Heuristic model for educational purposes — not predictive
          </p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur rounded-2xl p-6 border border-slate-700 shadow-2xl">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <TrendingUp size={20} className="text-cyan-400" />
            Scenario Space (Ω)
          </h2>
          
          <div className="space-y-4">
            {futures.map(future => (
              <div key={future.id} className="space-y-2">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{future.name}</span>
                    <span className="text-xs text-slate-400">
                      [{future.keywords.join(', ')}]
                    </span>
                  </div>
                  <span className="text-sm font-mono bg-slate-700 px-3 py-1 rounded">
                    {(future.probability * 100).toFixed(1)}%
                  </span>
                </div>
                
                <div className="relative h-8 bg-slate-700 rounded-lg overflow-hidden">
                  <div 
                    className={`absolute inset-y-0 left-0 bg-gradient-to-r ${future.color} transition-all duration-500 ease-out flex items-center justify-end pr-2`}
                    style={{ width: `${future.probability * 100}%` }}
                  >
                    {future.probability > 0.15 && (
                      <span className="text-xs font-bold text-white drop-shadow">
                        {future.coreLogic}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-800/50 backdrop-blur rounded-2xl p-6 border border-slate-700 shadow-2xl space-y-4">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <Zap size={20} className="text-yellow-400" />
            Argument Input → Probability Shift
          </h2>
          
          <div className="space-y-3">
            <textarea
              value={argument}
              onChange={(e) => setArgument(e.target.value)}
              placeholder="Enter argument to modify scenario probabilities..."
              className="w-full bg-slate-700 text-white rounded-lg p-3 border border-slate-600 focus:border-purple-500 focus:outline-none resize-none"
              rows={3}
            />
            
            <div className="flex items-center gap-2">
              <label className="text-sm text-slate-300">Resonance Strength:</label>
              <input
                type="range"
                min="1.2"
                max="3.0"
                step="0.1"
                value={resonanceStrength}
                onChange={(e) => setResonanceStrength(parseFloat(e.target.value))}
                className="flex-1"
              />
              <span className="text-sm font-mono bg-slate-700 px-2 py-1 rounded">{resonanceStrength.toFixed(1)}x</span>
            </div>
            
            <div className="flex gap-3">
              <button
                onClick={applyArgument}
                disabled={!argument.trim() || isAnimating}
                className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:from-slate-600 disabled:to-slate-600 text-white font-semibold py-3 rounded-lg transition-all transform hover:scale-105 disabled:scale-100 flex items-center justify-center gap-2"
              >
                <Zap size={18} />
                Apply Argument
              </button>
              
              <button
                onClick={sampleScenario}
                disabled={isAnimating}
                className="flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 disabled:from-slate-600 disabled:to-slate-600 text-white font-semibold py-3 rounded-lg transition-all transform hover:scale-105 disabled:scale-100 flex items-center justify-center gap-2"
              >
                <Sparkles size={18} />
                Sample Scenario
              </button>
              
              <button
                onClick={reset}
                className="bg-slate-700 hover:bg-slate-600 text-white p-3 rounded-lg transition-all"
                title="Reset"
              >
                <RotateCcw size={20} />
              </button>
            </div>
          </div>
        </div>

        {selectedScenario && (
          <div className="bg-gradient-to-r from-slate-800 to-purple-900 rounded-2xl p-6 border-2 border-purple-500 shadow-2xl">
            <h2 className="text-xl font-semibold mb-3 flex items-center gap-2">
              <Sparkles size={20} className="text-yellow-400" />
              Sampled Outcome (Stochastic Selection)
            </h2>
            <div className={`text-2xl font-bold bg-gradient-to-r ${selectedScenario.color} bg-clip-text text-transparent`}>
              {selectedScenario.name}
            </div>
            <div className="text-sm text-slate-300 mt-2">
              Core Logic: {selectedScenario.coreLogic}
            </div>
            <div className="text-xs text-slate-400 mt-2 italic">
              Note: This is a weighted random selection, not a prediction
            </div>
          </div>
        )}

        {history.length > 0 && (
          <div className="bg-slate-800/50 backdrop-blur rounded-2xl p-6 border border-slate-700 shadow-2xl">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Clock size={20} className="text-green-400" />
              Iteration History ({history.length} samples)
            </h2>
            
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {history.slice().reverse().map((entry, idx) => (
                <div key={idx} className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 text-sm">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex-1">
                      <div className="text-slate-300">Input Argument:</div>
                      <div className="text-white font-medium">{entry.argument}</div>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="text-cyan-400">Sampled:</span> {entry.sampledScenario}
                    </div>
                    <div>
                      <span className="text-purple-400">Synthetic Input:</span> {entry.syntheticInput}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="text-center text-xs text-slate-400 space-y-1">
          <p className="italic">Illustrative probabilistic framing (non-predictive):</p>
          <p className="font-mono">argmax_M P(M | Evidence, Argument)</p>
          <p className="text-purple-400 mt-2">Part of the Veritas Protocol ecosystem</p>
          <p className="text-slate-500">Demonstrating argument dynamics without ontological claims</p>
        </div>

      </div>
    </div>
  );
};

export default TemporalNavigationEngine;
