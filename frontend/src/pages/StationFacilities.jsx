import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { stations } from '../data/stations';
import Header from '../components/Header';
import Footer from '../components/Footer';

const StationFacilities = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [station, setStation] = useState(null);

  useEffect(() => {
    if (stations[id]) {
      setStation(stations[id]);
    } else {
      setTimeout(() => navigate('/stations'), 2000);
    }
  }, [id, navigate]);

  if (!station) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-xl text-slate-400 animate-pulse">Loading Station Data...</div>
      </div>
    );
  }

  // Filter out Waypoints (used only for routing geometry)
  const visibleFacilities = station.facilities.filter(f => !f.isHidden && f.category !== "Waypoint");

  // Group by category
  const groupedFacilities = visibleFacilities.reduce((acc, facility) => {
    if (!acc[facility.category]) acc[facility.category] = [];
    acc[facility.category].push(facility);
    return acc;
  }, {});

  // Category visual mapping
  const categoryConfig = {
    Platform: { border: "border-blue-500", bg: "bg-blue-500/10", text: "text-blue-400" },
    Exit: { border: "border-emerald-500", bg: "bg-emerald-500/10", text: "text-emerald-400" },
    Food: { border: "border-amber-500", bg: "bg-amber-500/10", text: "text-amber-400" },
    Utility: { border: "border-purple-500", bg: "bg-purple-500/10", text: "text-purple-400" },
    Stairs: { border: "border-orange-500", bg: "bg-orange-500/10", text: "text-orange-400" },
    Bridge: { border: "border-cyan-500", bg: "bg-cyan-500/10", text: "text-cyan-400" }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 15 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-between relative overflow-hidden font-sans">
      <Header />
      <main className="flex-grow w-full max-w-7xl mx-auto p-6 md:p-12 text-slate-200">
      
      {/* Header section */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto mb-12 flex flex-col md:flex-row items-start md:items-center justify-between border-b border-slate-800 pb-8"
      >
        <div>
          <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 to-cyan-400">
            {station.name}
          </h1>
          <p className="mt-2 text-slate-500 text-lg">Comprehensive Facilities Documentation</p>
        </div>

        <button 
          onClick={() => navigate(`/station/${id}`)}
          className="mt-6 md:mt-0 px-6 py-3 rounded-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold transition-colors shadow-[0_0_20px_-5px_rgba(16,185,129,0.4)] flex items-center"
        >
          View Interactive Blueprint
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 border border-emerald-400 rounded p-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
          </svg>
        </button>
      </motion.div>

      {/* Facilities Grid */}
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-20"
      >
        {Object.entries(groupedFacilities).map(([category, items]) => {
          const style = categoryConfig[category] || { border: "border-slate-500", bg: "bg-slate-500/10", text: "text-slate-400" };
          
          return (
            <motion.div 
              key={category} 
              variants={itemVariants}
              className={`bg-slate-900/50 backdrop-blur-md rounded-2xl border p-6 overflow-hidden relative shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 ${style.border.replace('border-', 'hover:border-')}`}
            >
              <div className={`absolute top-0 left-0 w-1.5 h-full ${style.bg} border-l-2 ${style.border}`}></div>
              
              <h2 className={`text-2xl font-bold mb-6 ml-4 ${style.text} flex items-center justify-between`}>
                {category}
                <span className={`text-xs px-3 py-1 rounded-full ${style.bg.replace('/10', '/30')} font-bold tracking-wider`}>
                  {items.length} {items.length === 1 ? 'PLACE' : 'PLACES'}
                </span>
              </h2>

              <ul className="space-y-4 ml-4">
                {items.sort((a,b) => a.name.localeCompare(b.name)).map((facility, index) => (
                  <li key={index} className="flex items-center text-slate-200 font-medium bg-slate-800/20 p-2 rounded-lg hover:bg-slate-800/50 transition-colors">
                    <span className={`w-2 h-2 rounded-full mr-3 ${style.bg.replace('/10', '')} shadow-[0_0_8px_rgba(255,255,255,0.2)]`}></span>
                    {facility.name}
                  </li>
                ))}
              </ul>
            </motion.div>
          );
        })}
      </motion.div>

      </main>
      <Footer />
    </div>
  );
};

export default StationFacilities;
