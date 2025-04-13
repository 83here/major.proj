import React from 'react';
import PredictionGraph from './components/PredictionGraph';
import './App.css';

function App() {
  return (
    <>
      <header>
        <h1>We are <span style={{ color: "var(--secondary)" }}>Machine Pulse</span></h1>
        <p>Predictive maintenance systems using Deep Learning Sequence Models</p>
      </header>

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

      <section>
        <h3>Predicted Accelerometer Data (X, Y, Z)</h3>
        <PredictionGraph />
      </section>
    </>
  );
}

export default App;
