import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { stations } from '../data/stations';
import Header from '../components/Header';
import Footer from '../components/Footer';

const StationSelection = () => {
  const navigate = useNavigate();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.2 }
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-between relative overflow-hidden font-sans">
      <Header />
      <main className="flex-grow flex flex-col items-center justify-center p-8 relative z-10 w-full max-w-7xl">

      <div className="mb-16 mt-8 text-center max-w-2xl">
        <motion.h1 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 to-cyan-400 mb-4"
        >
          Select Your Station
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-slate-400 text-lg"
        >
          Choose a station to view its real-time blueprint and navigate its facilities.
        </motion.p>
      </div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-5xl"
      >
        {Object.values(stations).map((station) => (
          <motion.div
            key={station.id}
            variants={cardVariants}
            className="group relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/50 p-8 shadow-xl transition-all hover:bg-slate-800/60 hover:border-emerald-500/50 hover:shadow-[0_0_30px_-10px_rgba(16,185,129,0.3)] backdrop-blur-sm flex flex-col justify-between"
          >
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 to-cyan-400 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-300"></div>
            
            <div>
              <h2 className="text-3xl font-bold text-slate-100 mb-2">{station.name}</h2>
              <div className="flex items-center gap-2 mb-6">
                <span className="px-3 py-1 text-xs font-semibold bg-emerald-900/50 text-emerald-300 rounded-full border border-emerald-800/50">
                  {station.facilities.filter(f => !f.isHidden && f.category !== "Waypoint").length} Facilities
                </span>
                <span className="px-3 py-1 text-xs font-semibold bg-slate-800 text-slate-300 rounded-full border border-slate-700">
                  Interactive Map
                </span>
              </div>
            </div>
            
            <div className="mt-8 grid grid-cols-2 gap-4">
              <button 
                onClick={() => navigate(`/station/${station.id}`)}
                className="flex items-center justify-center py-3 px-4 rounded-xl bg-emerald-600/10 border border-emerald-500/30 text-emerald-400 hover:bg-emerald-600 hover:text-white font-medium transition-all group/btn"
              >
                View Blueprint 
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 transform group-hover/btn:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
              
              <button 
                onClick={() => navigate(`/facilities/${station.id}`)}
                className="flex items-center justify-center py-3 px-4 rounded-xl bg-slate-800/50 border border-slate-700 text-slate-300 hover:bg-slate-700 hover:text-white font-medium transition-all group/btn2"
              >
                View Facilities
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 text-slate-400 group-hover/btn2:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </button>
            </div>
          </motion.div>
        ))}
      </motion.div>
      </main>
      <Footer />
    </div>
  );
};

export default StationSelection;
