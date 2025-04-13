import React from 'react';
import PredictionGraph from './components/PredictionGraph';
import './App.css';

function App() {
  return (
    <>
    <header>
      <h1>We are <span className="highlight">Machine Pulse</span></h1>
      <p>Predictive maintenance systems using Deep Learning Sequence Models</p>
    </header>

    <div className="dashboard-container">
      {/* Left Panel */}
      <aside className="left-panel">
        <section>
          <h2>What We Do</h2>
          <ul>
            <li>🔧 Industrial machines generate vibration signals that reflect their internal condition.</li>
            <li>⚠️ Traditional monitoring methods are reactive and inefficient.</li>
            <li>📈 Time-series forecasting, especially using sequence models (LSTM), helps detect early failure signs.</li>
            <li>🔍 Traditional systems learn from normal operating conditions and flag deviations.</li>
            <li>🔄 Our approach flips this paradigm — we train the model using historical failure data to learn how failures evolve.</li>
          </ul>
        </section>

        <section>
          <h2>Our Core Hypothesis</h2>
          <blockquote>
            "Machines often exhibit patchy notes of faulty vibrational behavior before transitioning into higher-order failures."
          </blockquote>
        </section>
      </aside>

      {/* Right Panel */}
      <main className="right-panel">
   

        <section>
          <PredictionGraph />
        </section>
      </main>
    </div>

    </>
  );
}

export default App;