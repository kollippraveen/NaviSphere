import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import MapViewer from '../components/MapViewer';
import { stations } from '../data/stations';
import Header from '../components/Header';
import Footer from '../components/Footer';

const StationView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const station = stations[id];

  const [startPoint, setStartPoint] = useState("");
  const [endPoint, setEndPoint] = useState("");
  const [navigationPath, setNavigationPath] = useState([]);
  const [isFindingPath, setIsFindingPath] = useState(false);

  if (!station) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-8">
        <h1 className="text-3xl text-red-500 font-bold mb-4">Station Not Found</h1>
        <button onClick={() => navigate('/stations')} className="text-blue-400 hover:text-blue-300 underline">
          Return to Selection
        </button>
      </div>
    );
  }

  const handleNavigate = async () => {
    if (!startPoint || !endPoint) {
      alert("Please select both a Start Point and Destination");
      return;
    }

    setIsFindingPath(true);
    try {
      const res = await axios.post('https://navisphere.onrender.com/navigate', {
        station_name: station.name,
        start: startPoint,
        destination: endPoint
      });
      if (res.data.path) {
        setNavigationPath(res.data.path);
      } else if (res.data.error) {
        alert(`Navigation error: ${res.data.error}`);
        setNavigationPath([]);
      }
    } catch (err) {
      // Backend returns {"error":"..."} for 404/400 – read it if available
      const serverMsg = err?.response?.data?.error;
      if (serverMsg) {
        alert(`Navigation error: ${serverMsg}`);
      } else {
        alert("Backend is unreachable. Make sure uvicorn is running on port 8000!");
      }
      setNavigationPath([]);
    } finally {
      setIsFindingPath(false);
    }
  };

  const handleNodeClick = (nodeName) => {
    if (!startPoint || (startPoint && endPoint)) {
      setStartPoint(nodeName);
      setEndPoint("");
      setNavigationPath([]);
    } else if (startPoint && !endPoint && nodeName !== startPoint) {
      setEndPoint(nodeName);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-between relative overflow-hidden font-sans text-white">
      <Header />
      <div className="flex-grow w-full max-w-7xl mx-auto p-8 relative z-10">
        <div className="mb-8 flex flex-col md:flex-row md:items-center justify-between">
          <div>
            <h1 className="text-4xl font-black text-emerald-400">{station.name}</h1>
            <p className="text-slate-400 mt-1">Navisphere Navigation System</p>
          </div>
        </div>

        <main className="grid grid-cols-1 lg:grid-cols-12 gap-8 max-w-7xl mx-auto">
          <div className="lg:col-span-8">
            <div className="bg-slate-950 rounded-2xl overflow-hidden border border-slate-800 shadow-2xl">
              <MapViewer
                mapUrl={station.mapUrl}
                facilities={station.facilities}
                path={navigationPath}
                highlighted={{ start: startPoint, end: endPoint }}
                onNodeClick={handleNodeClick}
              />
            </div>
          </div>
          <div className="lg:col-span-4 space-y-4">
            <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl">
              <h3 className="font-bold text-lg mb-4 text-slate-200 border-b border-slate-700 pb-2">Navigation Control</h3>
              <p className="text-sm text-slate-400 mb-6 italic">
                Select source and destination to find the shortest path.
              </p>
              <div className="space-y-4">
                <div>
                  <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-1 block">Start Point</label>
                  <select
                    className="w-full bg-slate-900 text-slate-200 border border-slate-700 p-3 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                    onChange={(e) => {
                      setStartPoint(e.target.value);
                      setNavigationPath([]);
                    }}
                    value={startPoint}
                  >
                    <option value="">Select Start</option>
                    {station.facilities.map(f => <option key={f.name} value={f.name}>{f.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-1 block">Destination</label>
                  <select
                    className="w-full bg-slate-900 text-slate-200 border border-slate-700 p-3 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                    onChange={(e) => {
                      setEndPoint(e.target.value);
                      setNavigationPath([]);
                    }}
                    value={endPoint}
                  >
                    <option value="">Select Goal</option>
                    {station.facilities.map(f => <option key={f.name} value={f.name}>{f.name}</option>)}
                  </select>
                </div>
                <button
                  onClick={handleNavigate}
                  disabled={isFindingPath}
                  className={`w-full font-bold py-4 rounded-xl shadow-lg transition-all transform active:scale-95 ${isFindingPath ? 'bg-slate-600 cursor-not-allowed' : 'bg-gradient-to-r from-emerald-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 hover:shadow-emerald-500/25 text-white'}`}
                >
                  {isFindingPath ? 'CALCULATING...' : 'FIND SHORTEST PATH'}
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default StationView;
