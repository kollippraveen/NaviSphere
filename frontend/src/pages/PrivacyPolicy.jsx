import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';

const PrivacyPolicy = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-between relative overflow-hidden font-sans">
      <Header />
      {/* Background Orbs */}
      <div className="absolute top-[-10%] right-[-10%] w-[30%] h-[30%] bg-emerald-600/10 blur-[100px] rounded-full pointer-events-none" />
      
      {/* Main Content */}
      <main className="flex-grow flex flex-col items-center justify-center p-8 relative z-10 w-full">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-3xl mx-auto z-10 relative bg-slate-900/30 backdrop-blur-sm border border-slate-800 p-8 md:p-12 rounded-3xl"
      >
        <h1 className="text-4xl font-bold text-slate-100 mb-8 border-b border-slate-800 pb-6">Privacy Policy</h1>
        
        <div className="space-y-6 text-slate-300 font-light leading-relaxed">
          <p>
            <strong className="text-slate-200 font-semibold">Last Updated: Navisphere v1.0</strong>
          </p>
          
          <h2 className="text-2xl font-semibold text-emerald-400 mt-8 mb-4">1. Information We Collect</h2>
          <p>
            Navisphere operates as a purely client-side spatial routing application. We do not store, track, or harvest any personal data, location tracking information, or user behavioral analytics. Your privacy is paramount.
          </p>
          
          <h2 className="text-2xl font-semibold text-emerald-400 mt-8 mb-4">2. Use of Routing Data</h2>
          <p>
            The path calculations requested between two station facilities (e.g., 'Entry 1' to 'Platform 4') are processed ephemerally on our backend Dijkstra algorithm service. This data is not logged or associated with any user identity.
          </p>
          
          <h2 className="text-2xl font-semibold text-emerald-400 mt-8 mb-4">3. Cookies and Tracking</h2>
          <p>
            Navisphere does not employ the use of tracking cookies, third-party analytics scripts, or advertising trackers. Session state regarding the currently viewed blueprint is stored locally in your browser's ephemeral memory.
          </p>

          <h2 className="text-2xl font-semibold text-emerald-400 mt-8 mb-4">4. Updates to Privacy</h2>
          <p>
            Any future changes to this privacy policy will be documented clearly on this page. By continuing to use Navisphere, you agree to the conditions outlined herein.
          </p>
        </div>
      </motion.div>
      </main>

      <Footer />
    </div>
  );
};

export default PrivacyPolicy;
