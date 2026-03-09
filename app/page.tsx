"use client";
import { useEffect } from 'react';
import Link from 'next/link';
import { Activity, ShieldCheck, ArrowRight, Zap, HeartPulse, BrainCircuit } from 'lucide-react';

export default function Home() {
  
  // This effect handles "Fade In on Scroll"
  useEffect(() => {
    const observerOptions = {
      threshold: 0.1,
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('opacity-100', 'translate-y-0');
          entry.target.classList.remove('opacity-0', 'translate-y-10');
        }
      });
    }, observerOptions);

    const targets = document.querySelectorAll('.scroll-reveal');
    targets.forEach((target) => observer.observe(target));

    return () => observer.disconnect();
  }, []);

  return (
    <div className="min-h-screen bg-white font-sans selection:bg-blue-100 overflow-x-hidden">
      <div className="bg-blue-600 text-white text-center py-2 text-xs font-black uppercase tracking-[0.2em] animate-pulse">
        Live Production Environment: MedAI Studio v1.0
      </div>

      <nav className="flex justify-between items-center px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="bg-blue-600 p-2 rounded-xl shadow-lg group-hover:rotate-[360deg] transition-transform duration-700">
            <Activity className="text-white" size={24} />
          </div>
          <span className="text-2xl font-bold text-slate-800 tracking-tighter italic">
            MedAI<span className="text-blue-600 not-italic font-black">Studio</span>
          </span>
        </div>
        <Link href="/diagnose">
          <button className="bg-slate-900 text-white px-6 py-2.5 rounded-full font-bold hover:bg-blue-600 transition-all shadow-xl active:scale-95 hover:-translate-y-1">
            Launch AI
          </button>
        </Link>
      </nav>

      <section className="relative px-6 pt-16 pb-24 max-w-7xl mx-auto text-center">
        {/* HERO REVEAL ANIMATION */}
        <div className="scroll-reveal opacity-0 translate-y-10 transition-all duration-[1000ms] ease-out">
          <div className="inline-flex items-center gap-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-xs font-black uppercase tracking-widest mb-8 border border-blue-100">
            <ShieldCheck size={14} className="animate-bounce" />
            Verified Clinical Intelligence
          </div>

          <h1 className="text-6xl md:text-8xl font-black text-slate-900 leading-[0.95] tracking-tight mb-8">
            Healthcare <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
              Decoded by AI.
            </span>
          </h1>

          <p className="text-xl text-slate-500 leading-relaxed max-w-2xl mx-auto mb-12">
            Experience instant diagnostic insights. Our Random Forest model analyzes your symptoms against clinical data patterns in milliseconds.
          </p>

          <div className="flex justify-center mb-24">
            <Link href="/diagnose">
              <button className="bg-blue-600 text-white px-10 py-5 rounded-2xl font-black text-xl hover:bg-slate-900 transition-all shadow-2xl shadow-blue-200 flex items-center gap-3 active:scale-95 group">
                Check Symptoms Now
                <ArrowRight size={22} className="group-hover:translate-x-2 transition-transform" />
              </button>
            </Link>
          </div>
        </div>

        {/* FEATURES GRID WITH SCROLL REVEAL */}
        <div className="grid md:grid-cols-3 gap-8 text-left">
          {[
            { icon: <Zap />, title: "Instant Analysis", color: "hover:border-blue-400" },
            { icon: <HeartPulse />, title: "131+ Conditions", color: "hover:border-rose-400" },
            { icon: <BrainCircuit />, title: "Neural Logic", color: "hover:border-indigo-400" }
          ].map((item, i) => (
            <div 
              key={i} 
              className={`scroll-reveal opacity-0 translate-y-10 transition-all duration-[800ms] p-10 border border-slate-100 rounded-[2.5rem] bg-white shadow-sm hover:shadow-2xl hover:-translate-y-4 group cursor-default ${item.color}`}
              style={{ transitionDelay: `${i * 200}ms` }}
            >
              <div className="bg-slate-50 w-14 h-14 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500">
                {item.icon}
              </div>
              <h3 className="font-black text-xl text-slate-900 mb-3">{item.title}</h3>
              <p className="text-slate-500 leading-relaxed text-sm">Proprietary logic identifies symptom clusters with high accuracy.</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="py-12 text-center text-slate-400 text-sm font-medium border-t border-slate-50">
        © 2026 MedAI Studio • Powered by Clinical Intelligence
      </footer>
    </div>
  );
}