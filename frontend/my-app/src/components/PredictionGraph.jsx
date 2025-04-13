import React, { useEffect, useState } from 'react';
// import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const PredictionGraph = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchPrediction = async () => {
        try {
          // MOCK RESPONSE — simulates what the backend will eventually return
          const mockResponse = {
            data: {
              message: "Prediction successful",
              current_data: [
                [0.1, 0.2, 0.3], [0.2, 0.3, 0.1], [0.3, 0.1, 0.2], [0.4, 0.3, 0.2],
                [0.5, 0.4, 0.3], [0.6, 0.5, 0.4], [0.7, 0.6, 0.5], [0.8, 0.7, 0.6],
                [0.9, 0.8, 0.7], [1.0, 0.9, 0.8]
              ],
              prediction: [
                [1.1, 1.0, 0.9],
                [1.2, 1.1, 1.0],
                [1.3, 1.2, 1.1],
                [1.4, 1.3, 1.2],
                [1.5, 1.4, 1.3],
              ]
            }
          };
      
          // You can toggle this: 
          // const res = await axios.get("http://localhost:8000/predict");
          const res = mockResponse;
      
          if (res.data.prediction) {
            const formatted = res.data.prediction.map((entry, index) => ({
              time: index + 1,
              x: entry[0],
              y: entry[1],
              z: entry[2]
            }));
            setData(formatted);
          }
        } catch (error) {
          console.error("Error fetching prediction:", error);
        }
      };
      

    fetchPrediction();

    const interval = setInterval(fetchPrediction, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h3>Predicted Accelerometer Data (X, Y, Z)</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="x" stroke="#8884d8" />
          <Line type="monotone" dataKey="y" stroke="#82ca9d" />
          <Line type="monotone" dataKey="z" stroke="#ffc658" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionGraph;
