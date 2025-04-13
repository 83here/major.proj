import React, { useEffect, useState } from 'react';
import PredictionGraph from './components/PredictionGraph';
import './App.css';

function App() {
  const [mse, setMSE] = useState(0);
  const [status, setStatus] = useState({ label: '', color: '' });

  // Mock API that returns a simulated MSE value
  const fetchMockMSE = () => {
    // Random number between 0 and 7 (simulate mean square error)
    return (Math.random() * 7).toFixed(2);
  };

  // Update the health status based on MSE
  const updateHealthStatus = (value) => {
    const mseValue = parseFloat(value);

    if (mseValue < 2) {
      setStatus({ label: '❌ Critical – Stop Machine', color: 'red' });
    } else if (mseValue < 3) {
      setStatus({ label: '🔧 Needs Immediate Repair', color: 'orange' });
    } else if (mseValue < 4) {
      setStatus({ label: '⚠️ Needs Minor Repair', color: 'yellow' });
    } else if (mseValue < 6) {
      setStatus({ label: '👍 Good', color: 'lime' });
    } else {
      setStatus({ label: '✅ Excellent', color: 'green' });
    }
  };

  // Polling the mock API every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      const mseValue = fetchMockMSE();
      setMSE(mseValue);
      updateHealthStatus(mseValue);
    }, 5000);

    // initial fetch
    const mseValue = fetchMockMSE();
    setMSE(mseValue);
    updateHealthStatus(mseValue);

    return () => clearInterval(interval);
  }, []);

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
          <h3>Motor Health Status</h3>
          <div className={`status-card ${status.color}`}>
            <p>{status.label}</p>
            <small style={{ display: 'block', marginTop: '0.5rem', fontSize: '0.9rem', color: '#fff' }}>
              Current MSE: {mse}
            </small>
          </div>
        </section>

        <section>
          <h3>Predicted Machine Data (X, Y, Z)</h3>
          <PredictionGraph />
        </section>
      </main>
    </div>

    </>
  );
}

export default App;