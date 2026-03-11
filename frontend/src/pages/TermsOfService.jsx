import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';

const TermsOfService = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-between relative overflow-hidden font-sans">
      <Header />
      {/* Background Orbs */}
      <div className="absolute top-[-10%] right-[-10%] w-[30%] h-[30%] bg-cyan-600/10 blur-[100px] rounded-full pointer-events-none" />
      
      {/* Main Content */}
      <main className="flex-grow flex flex-col items-center justify-center p-8 relative z-10 w-full">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-3xl mx-auto z-10 relative bg-slate-900/30 backdrop-blur-sm border border-slate-800 p-8 md:p-12 rounded-3xl"
      >
        <h1 className="text-4xl font-bold text-slate-100 mb-8 border-b border-slate-800 pb-6">Terms of Service</h1>
        
        <div className="space-y-6 text-slate-300 font-light leading-relaxed">
          <p>
            <strong className="text-slate-200 font-semibold">Effective Date: Navisphere Launch</strong>
          </p>
          
          <h2 className="text-2xl font-semibold text-cyan-400 mt-8 mb-4">1. Acceptance of Terms</h2>
          <p>
            By accessing or using the Navisphere platform, you agree to be bound by these Terms of Service. If you disagree with any part of the terms, you must not access the application.
          </p>
          
          <h2 className="text-2xl font-semibold text-cyan-400 mt-8 mb-4">2. Map Accuracy Disclaimer</h2>
          <p>
            Navisphere strives to provide highly accurate, mathematically validated spatial distances and pathfinding based on official station blueprints. However, real-world physical blockages, construction, or temporary facility closures may occur that are not reflected in the digital graph. Navisphere is not liable for missed transport connections resulting from navigational reliance.
          </p>
          
          <h2 className="text-2xl font-semibold text-cyan-400 mt-8 mb-4">3. Prohibited Uses</h2>
          <p>
            You agree not to use the service to:
            <ul className="list-disc pl-8 mt-2 space-y-2">
              <li>Attempt to reverse engineer the routing APIs.</li>
              <li>Scrape or bulk download spatial graph node data.</li>
              <li>Exploit backend services by launching denial-of-service (DDoS) requests against the routing endpoints.</li>
            </ul>
          </p>

          <h2 className="text-2xl font-semibold text-cyan-400 mt-8 mb-4">4. Intellectual Property</h2>
          <p>
            The custom architectural mapping interfaces, original SVG overlays, and unique UI/UX styling present in Navisphere are protected copyright. Unauthorized replication of the Navisphere brand aesthetic is prohibited.
          </p>
        </div>
      </motion.div>
      </main>

      <Footer />
    </div>
  );
};

export default TermsOfService;
