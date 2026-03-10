"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, Activity, Search } from 'lucide-react';

export default function SymptomChecker() {
  const [symptomsList, setSymptomsList] = useState<string[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [prediction, setPrediction] = useState("");
  const [description, setDescription] = useState("");
  const [precautions, setPrecautions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch('/api/main')
      .then(res => res.json())
      .then(data => {
        // Just set the symptoms directly!
        setSymptomsList(data.symptoms || []);
      })
      .catch(err => console.error("Backend offline", err));
  }, []);

  const handleToggle = (s: string) => {
    setSelected(prev => prev.includes(s) ? prev.filter(item => item !== s) : [...prev, s]);
  };

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/main", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: selected }),
      });
      
      const data = await response.json();
      
      setPrediction(data.prediction);
      setDescription(data.description);
      setPrecautions(data.precautions || []);
    } catch (error) {
      setPrediction("Server Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-4xl mx-auto">
        <Link href="/" className="inline-flex items-center text-slate-500 hover:text-blue-600 mb-8 transition font-bold">
          <ArrowLeft size={20} className="mr-2" /> Back to Home
        </Link>

        <div className="bg-white shadow-2xl rounded-[3rem] p-8 md:p-12 border border-slate-100">
          <header className="mb-10 text-center">
            <h1 className="text-4xl font-black text-slate-900">AI Symptom Analysis</h1>
            <p className="text-slate-500 mt-2">Select all symptoms you are currently experiencing.</p>
          </header>

          <div className="relative mb-8">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
            <input 
              type="text"
              placeholder="Search symptoms (e.g. fever, headache)..."
              className="w-full pl-12 pr-4 py-4 rounded-2xl border-2 border-slate-50 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all font-medium"
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="space-y-6">
            <div className="flex flex-wrap gap-2 max-h-96 overflow-y-auto p-2 scrollbar-hide">
              {symptomsList
                .filter(s => s.toLowerCase().includes(searchTerm.toLowerCase()))
                .map(s => (
                  <button key={s} onClick={() => handleToggle(s)}
                    className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all border ${
                      selected.includes(s) ? 'bg-blue-600 text-white border-blue-600 shadow-lg scale-105' : 'bg-white text-slate-600 border-slate-200 hover:border-blue-400'
                    }`}>
                    <span className="capitalize">{s}</span>
                  </button>
                ))}
            </div>

            <button onClick={handleAnalyze} disabled={loading || selected.length === 0}
              className="w-full bg-slate-900 text-white font-black py-5 rounded-2xl hover:bg-blue-600 disabled:bg-slate-200 transition-all shadow-xl active:scale-[0.98] text-lg">
              {loading ? "Analyzing Medical Data..." : `Analyze ${selected.length} Selected Symptoms`}
            </button>

            {prediction && (
              <div className="mt-8 p-8 bg-blue-600 rounded-[2.5rem] text-white shadow-2xl animate-in fade-in slide-in-from-bottom-4">
                <h3 className="text-blue-100 font-black text-xs uppercase tracking-widest mb-2">Diagnosis Result</h3>
                <p className="text-4xl font-black mb-4">{prediction}</p>
                <div className="bg-white/10 p-6 rounded-2xl mb-6">
                    <p className="text-blue-50 text-sm leading-relaxed">{description}</p>
                </div>
                <div className="grid sm:grid-cols-2 gap-3">
                  {precautions.map((p, i) => (
                    <div key={i} className="bg-white/20 p-4 rounded-xl text-xs font-bold flex items-center gap-3 backdrop-blur-sm">
                      <div className="h-2 w-2 bg-white rounded-full"></div> {p}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}