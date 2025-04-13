import React, { useEffect, useState} from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const generateMockPrediction = (offset = 0) => {
  const prediction = Array.from({ length: 10 }, (_, i) => {
    const base = i + offset;
    return [
      Math.sin(base / 3) + Math.random() * 0.1,   // x
      Math.cos(base / 3) + Math.random() * 0.1,   // y
      Math.sin(base / 2) + Math.random() * 0.1    // z
    ];
  });
  return {
    data: {
      message: "Prediction successful",
      prediction,
    }
  };
};

const PredictionGraph = () => {
  const [dataX, setDataX] = useState([]);
  const [dataY, setDataY] = useState([]);
  const [dataZ, setDataZ] = useState([]);
  const [counter, setCounter] = useState(0);

  // Initialize with some data to ensure the charts have something to render
  useEffect(() => {
    const initialData = generateMockPrediction(0).data.prediction;
    
    const formattedX = initialData.map((entry, index) => ({
      time: index + 1,
      value: entry[0]
    }));
    
    const formattedY = initialData.map((entry, index) => ({
      time: index + 1,
      value: entry[1]
    }));
    
    const formattedZ = initialData.map((entry, index) => ({
      time: index + 1,
      value: entry[2]
    }));
    
    setDataX(formattedX);
    setDataY(formattedY);
    setDataZ(formattedZ);
    setCounter(initialData.length);
  }, []);

  useEffect(() => {
    const fetchPrediction = () => {
      try {
        const res = generateMockPrediction(counter);
        if (res.data.prediction) {
          const prediction = res.data.prediction;
          
          const formattedX = prediction.map((entry, index) => ({
            time: counter + index + 1,
            value: entry[0]
          }));
          
          const formattedY = prediction.map((entry, index) => ({
            time: counter + index + 1,
            value: entry[1]
          }));
          
          const formattedZ = prediction.map((entry, index) => ({
            time: counter + index + 1,
            value: entry[2]
          }));
          
          setDataX(prev => [...prev.slice(-20), ...formattedX].slice(-30));
          setDataY(prev => [...prev.slice(-20), ...formattedY].slice(-30));
          setDataZ(prev => [...prev.slice(-20), ...formattedZ].slice(-30));
          
          setCounter(counter + prediction.length);
        }
      } catch (error) {
        console.error("Error fetching prediction:", error);
      }
    };
    
    // Don't run immediately after initial mount (avoid double data)
    if (counter > 0) {
      const interval = setInterval(fetchPrediction, 2000);
      return () => clearInterval(interval);
    }
  }, [counter]);

  // Check if we have data to display
  const hasData = dataX.length > 0 && dataY.length > 0 && dataZ.length > 0;

  if (!hasData) {
    return <div className="p-4">Loading data...</div>;
  }

  return (
    <div className="p-4">
      
      <div className="mb-8">
        <h4 className="text-lg font-medium mb-2">X Axis</h4>
        <div style={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <LineChart data={dataX}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time"   label={{ value: 'Time', position: 'insideBottomRight', offset: -5 }}/>
              <YAxis domain={[-1.5, 1.5]}   label={{ value: 'Vibration Strength', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#8884d8" 
                dot={false} 
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div className="mb-8">
        <h4 className="text-lg font-medium mb-2">Y Axis</h4>
        <div style={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <LineChart data={dataY}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time"  label={{ value: 'Time', position: 'insideBottomRight', offset: -5 }} />
              <YAxis domain={[-1.5, 1.5]}  label={{ value: 'Vibration Strength ', angle: -90, position: 'insideLeft'}} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#82ca9d" 
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div className="mb-8">
        <h4 className="text-lg font-medium mb-2">Z Axis</h4>
        <div style={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <LineChart data={dataZ}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time"   label={{ value: 'Time', position: 'insideBottomRight', offset: -5 }}/>
              <YAxis domain={[-1.5, 1.5]}   label={{ value: 'Vibration Strength', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#ffc658" 
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default PredictionGraph;