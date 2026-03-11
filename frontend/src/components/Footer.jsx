import React from 'react';
import { useNavigate } from 'react-router-dom';

const Footer = () => {
  const navigate = useNavigate();

  return (
    <footer className="w-full relative z-20 py-6 px-8 border-t border-white/5 bg-slate-950/60 backdrop-blur-md flex flex-col md:flex-row items-center justify-between text-slate-500 text-sm">
      <p>&copy; {new Date().getFullYear()} Navisphere. All rights reserved.</p>
      <div className="flex gap-6 mt-4 md:mt-0">
        <span className="hover:text-emerald-400 cursor-pointer transition-colors" onClick={() => navigate('/privacy')}>Privacy Policy</span>
        <span className="hover:text-emerald-400 cursor-pointer transition-colors" onClick={() => navigate('/terms')}>Terms of Service</span>
      </div>
    </footer>
  );
};

export default Footer;
