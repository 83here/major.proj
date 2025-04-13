import React, { useEffect, useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import axios from 'axios';

const PredictionGraph = () => {
  const [dataX, setDataX] = useState([]);
  const [dataY, setDataY] = useState([]);
  const [dataZ, setDataZ] = useState([]);
  const [tick, setTick] = useState(0); // Force rerender
  const [breakdownTimer, setBreakdownTimer] = useState(0);
  const [mseBelowThreshold, setMseBelowThreshold] = useState(false);
  const [showAlert, setShowAlert] = useState(false);


  const [mse, setMSE] = useState(0);
const [status, setStatus] = useState({ label: '', color: '' });

const calculateMSE = (current, predicted) => {
  let error = 0;
  const len = Math.min(5, current.length, predicted.length); // Just in case

  for (let i = 0; i < len; i++) {
    const curr = current[current.length - 5 + i];
    const pred = predicted[i];

    const dx = curr[0] - pred[0];
    const dy = curr[1] - pred[1];
    const dz = curr[2] - pred[2];

    error += dx * dx + dy * dy + dz * dz;
  }

  return (error / (len * 3)).toFixed(2); // 3 axes
};

const updateHealthStatus = (value) => {
  const mseValue = parseFloat(value);

  setMseBelowThreshold(mseValue < 2); // only tracking this now

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
useEffect(() => {
  const interval = setInterval(() => {
    if (mseBelowThreshold) {
      setBreakdownTimer(prev => {
        const updated = prev + 1;
        if (updated >= 10) {
          setShowAlert(true);
        }
        return updated;
      });
    } else {
      setBreakdownTimer(0);
      setShowAlert(false);
    }
  }, 1000);

  return () => clearInterval(interval);
}, [mseBelowThreshold]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get('http://0.0.0.0:8000/predict');
        const current = res.data.current_data.map(d => d[0]);
        const predicted = res.data.prediction;

        const formattedX = [];
        const formattedY = [];
        const formattedZ = [];

        // Add current data from time 1 to current.length
        current.forEach((entry, i) => {
          formattedX.push({ time: i + 1, value: entry[0], type: 'current' });
          formattedY.push({ time: i + 1, value: entry[1], type: 'current' });
          formattedZ.push({ time: i + 1, value: entry[2], type: 'current' });
        });

        // Ensure prediction starts from time = 11
        predicted.forEach((entry, i) => {
          const t = 10 + i;
          formattedX.push({ time: t, value: entry[0], type: 'predicted' });
          formattedY.push({ time: t, value: entry[1], type: 'predicted' });
          formattedZ.push({ time: t, value: entry[2], type: 'predicted' });
        });

        const mseVal = calculateMSE(current, predicted);
        setMSE(mseVal);
        updateHealthStatus(mseVal);

        setDataX(formattedX);
        setDataY(formattedY);
        setDataZ(formattedZ);
        setTick(prev => prev + 1);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  const hasData = dataX.length > 0;

  if (!hasData) return <div className="p-4">Loading data...</div>;

  const renderChart = (data, label, color) => {
    const current = data.filter(d => d.type === 'current');
    const predicted = data.filter(d => d.type === 'predicted');

    return (
      <div className="mb-8">
        <h4 className="text-lg font-medium mb-2">{label} Axis</h4>
        <div style={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <LineChart key={tick} data={[...current, ...predicted]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="time"
                domain={[1, 15]}
                type="number"
                label={{ value: 'Time (s)', position: 'insideBottomRight', offset: -5 }}
              />
              <YAxis
                domain={[-1.5, 1.5]}
                label={{ value: 'Vibration', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip />
              <Legend />
              <Line
                data={current}
                type="monotone"
                dataKey="value"
                stroke={color}
                dot={false}
                isAnimationActive={false}
                name="Current"
              />
              <Line
                data={predicted}
                type="monotone"
                dataKey="value"
                stroke="#ff0000"
                strokeDasharray="5 5"
                dot={false}
                isAnimationActive={false}
                name="Predicted"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };
  console.log(showAlert,'alret')
  return (
    <div className="p-4">
      {showAlert && (
  <div className="alert bg-red-700 text-white p-4 rounded-xl shadow-lg  my-12">
    🚨 <strong>Machine Breakdown Alert:</strong> 
  </div>
)}
       <section>
          <h3>Motor Health Status</h3>
          <div className={`status-card ${status.color}`}>
            <p>{status.label}</p>
            <small style={{ display: 'block', marginTop: '0.5rem', fontSize: '0.9rem', color: '#fff' }}>
              Current MSE: {mse}
            </small>
          </div>
        </section>
        <h3>Predicted Machine Data (X, Y, Z)</h3>
      {renderChart(dataX, 'X', '#8884d8')}
      {renderChart(dataY, 'Y', '#82ca9d')}
      {renderChart(dataZ, 'Z', '#ffc658')}
    </div>
  );
};

export default PredictionGraph;
