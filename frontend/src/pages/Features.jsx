import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Features = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: "Real-time Pathfinding",
      description: "Harness the power of Dijkstra's algorithm to calculate the absolute shortest walkable 90-degree orthogonal path between any two points in the station.",
      icon: "🎯"
    },
    {
      title: "Granular Facility Mapping",
      description: "Don't just find 'Platform 1'. Navigate exactly to the 'Cloak Room on Platform 1', specific food stalls, or remote escalators.",
      icon: "🗺️"
    },
    {
      title: "Interactive Architecture Maps",
      description: "View high-resolution, scale-accurate station blueprints overlaid with our interactive glowing 2D node-graph technology.",
      icon: "🏢"
    },
    {
      title: "Complete Documentation",
      description: "Access our beautiful 'View Facilities' documentation hub to instantly read through all available amenities without scrolling a map.",
      icon: "📚"
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-between relative overflow-hidden font-sans">
      <Header />
      {/* Background Orbs */}
      <div className="absolute top-0 right-0 w-[40%] h-[40%] bg-emerald-600/20 blur-[120px] rounded-full point-events-none" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-cyan-600/20 blur-[120px] rounded-full point-events-none" />

      {/* Main Content */}
      <main className="flex-grow flex flex-col items-center py-20 px-8 relative z-10 w-full">      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center z-10 mb-16 max-w-2xl"
      >
        <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 to-cyan-400 mb-6 drop-shadow-lg">
          Platform Features
        </h1>
        <p className="text-lg text-slate-400 leading-relaxed">
          Navisphere isn't just a map. It's a mathematically optimized spatial graph designed to eliminate terminal confusion layout entirely.
        </p>
      </motion.div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl z-10"
      >
        {features.map((feature, index) => (
          <motion.div 
            key={index}
            variants={itemVariants}
            className="bg-slate-900/40 backdrop-blur-md rounded-2xl p-8 border border-white/5 shadow-xl hover:shadow-[0_0_30px_rgba(16,185,129,0.15)] hover:border-emerald-500/30 transition-all duration-300"
          >
            <div className="text-4xl mb-6">{feature.icon}</div>
            <h2 className="text-2xl font-bold text-slate-200 mb-4">{feature.title}</h2>
            <p className="text-slate-400 leading-relaxed font-light">{feature.description}</p>
          </motion.div>
        ))}
      </motion.div>

      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        onClick={() => navigate('/stations')}
        className="mt-16 z-10 px-8 py-4 bg-gradient-to-r from-emerald-600 to-cyan-600 rounded-full text-white font-bold tracking-wide shadow-[0_0_20px_rgba(6,182,212,0.4)] hover:shadow-[0_0_30px_rgba(16,185,129,0.6)] transition-all hover:scale-105"
      >
        Experience Navisphere
      </motion.button>
      </main>

      <Footer />
    </div>
  );
};

export default Features;
