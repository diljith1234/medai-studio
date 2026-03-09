const AboutSection = () => (
  <section id="about" className="py-20 bg-white">
    <div className="max-w-5xl mx-auto px-6">
      <h2 className="text-3xl font-bold text-slate-900 mb-6 text-center">About Our AI Technology</h2>
      <div className="grid md:grid-cols-2 gap-12 items-center">
        <div>
          <p className="text-slate-600 leading-relaxed mb-4">
            Our diagnostic engine uses a <strong>Random Forest Machine Learning model</strong> trained on 
            thousands of clinical data points. Unlike a simple search, it analyzes the 
            <em>correlation</em> between multiple symptoms simultaneously.
          </p>
          <ul className="space-y-3">
            <li className="flex items-center text-sm text-slate-700">
              <span className="text-green-500 mr-2">✔</span> 132+ Symptoms Analyzed
            </li>
            <li className="flex items-center text-sm text-slate-700">
              <span className="text-green-500 mr-2">✔</span> Instant Precautions & Advice
            </li>
            <li className="flex items-center text-sm text-slate-700">
              <span className="text-green-500 mr-2">✔</span> Powered by Kaggle Health Dataset
            </li>
          </ul>
        </div>
        <div className="bg-slate-100 p-8 rounded-3xl border border-slate-200">
          <div className="text-4xl font-black text-blue-600 mb-2">95%</div>
          <p className="text-slate-500 text-sm italic">Accuracy rate based on validation datasets.</p>
        </div>
      </div>
    </div>
  </section>
);