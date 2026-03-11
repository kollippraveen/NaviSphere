import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Welcome = () => {
  const navigate = useNavigate();

  const text = "Welcome to NAVISPHERE";
  
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const letterVariants = {
    hidden: { opacity: 0, y: 50, rotateX: -90 },
    visible: {
      opacity: 1,
      y: 0,
      rotateX: 0,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 200,
      },
    },
  };

  const floatingVariants = {
    animate: {
      y: [0, -20, 0],
      rotate: [0, 5, -5, 0],
      transition: {
        duration: 5,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const floatingVariants2 = {
    animate: {
      y: [0, 30, 0],
      rotate: [0, -10, 10, 0],
      transition: {
        duration: 7,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col relative overflow-hidden font-sans">
      {/* Background Gradient Orbs (Emerald / Cyan / Purple) */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-emerald-600/30 blur-[140px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-20%] left-[20%] w-[40%] h-[40%] bg-cyan-600/20 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute top-[20%] right-[-10%] w-[40%] h-[50%] bg-fuchsia-600/20 blur-[140px] rounded-full pointer-events-none" />
      
      {/* 3D Floating Elements in Background */}
      <motion.div variants={floatingVariants} animate="animate" className="absolute top-[25%] left-[15%] w-24 h-24 bg-gradient-to-br from-emerald-400/20 to-transparent border border-emerald-500/30 rounded-2xl backdrop-blur-md rotate-12 pointer-events-none shadow-[0_0_30px_rgba(16,185,129,0.2)]" />
      <motion.div variants={floatingVariants2} animate="animate" className="absolute bottom-[30%] right-[15%] w-32 h-32 bg-gradient-to-tr from-cyan-400/20 to-transparent border border-cyan-500/30 rounded-full backdrop-blur-md pointer-events-none shadow-[0_0_40px_rgba(6,182,212,0.2)]" />
      <motion.div variants={floatingVariants} animate="animate" style={{animationDelay: '2s'}} className="absolute bottom-[15%] left-[30%] w-16 h-16 bg-gradient-to-bl from-fuchsia-400/20 to-transparent border border-fuchsia-500/30 rounded-xl backdrop-blur-md rotate-45 pointer-events-none shadow-[0_0_20px_rgba(217,70,239,0.2)]" />

      {/* Header */}
      <Header />

      {/* Main Content (Center) */}
      <main className="flex-grow flex flex-col items-center justify-center p-8 relative z-10 w-full overflow-hidden perspective-1000">
        
        {/* 3D Glass Card Container */}
        <motion.div 
          initial={{ opacity: 0, rotateX: 20, y: 50 }}
          animate={{ opacity: 1, rotateX: 0, y: 0 }}
          transition={{ duration: 1, ease: "easeOut" }}
          style={{ transformStyle: 'preserve-3d' }}
          className="relative max-w-4xl text-center bg-slate-900/40 backdrop-blur-xl border border-white/10 p-12 md:p-16 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.5),inset_0_2px_20px_rgba(255,255,255,0.05)]"
        >
          <motion.div
             variants={containerVariants}
             initial="hidden"
             animate="visible"
             className="flex justify-center flex-wrap mb-8 gap-x-4 md:gap-x-6 gap-y-2"
          >
            {["Welcome", "to", "NAVISPHERE"].map((word, wordIndex) => (
              <div key={wordIndex} className="flex whitespace-nowrap">
                {word.split("").map((char, charIndex) => {
                  const isNavisphere = word === 'NAVISPHERE';
                  return (
                    <motion.span
                      key={charIndex}
                      variants={letterVariants}
                      className={`text-5xl md:text-7xl lg:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-b drop-shadow-2xl ${isNavisphere ? 'from-emerald-300 to-cyan-500' : 'from-slate-100 to-slate-400'}`}
                      style={{ textShadow: isNavisphere ? '0 10px 30px rgba(16,185,129,0.3)' : 'none' }}
                    >
                      {char}
                    </motion.span>
                  );
                })}
              </div>
            ))}
          </motion.div>

          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 2.2, duration: 0.8 }}
            className="text-lg md:text-xl lg:text-2xl text-slate-300 mb-12 leading-relaxed max-w-2xl mx-auto font-light"
          >
            Navigate complex railway stations with absolute precision. Experience real-time blueprint pathfinding and interactive 3D visualizations designed for the modern commuter.
          </motion.p>

          <motion.button
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 2.7, duration: 0.5 }}
            whileHover={{ scale: 1.05, translateY: -2 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/stations')}
            className="relative group inline-flex items-center justify-center"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-full blur opacity-60 group-hover:opacity-100 transition duration-300"></div>
            <div className="relative bg-gradient-to-r from-emerald-500 to-cyan-600 border border-emerald-400/50 text-white font-bold py-4 px-10 rounded-full text-lg shadow-[0_10px_20px_-10px_rgba(16,185,129,0.5)] flex items-center gap-3">
              Start Journey
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </div>
          </motion.button>
        </motion.div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Welcome;
