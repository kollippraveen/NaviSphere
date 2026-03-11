import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className="w-full relative z-50 px-8 py-6 flex items-center justify-between backdrop-blur-md bg-slate-950/40 border-b border-white/5">
      <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-cyan-500 shadow-[0_0_15px_rgba(16,185,129,0.5)] flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-slate-900" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
          </svg>
        </div>
        <span className="text-xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 to-cyan-300 tracking-wider">
          NAVISPHERE
        </span>
      </div>
      <nav className="hidden md:flex gap-8 text-sm font-medium text-slate-300">
        <span className="cursor-pointer hover:text-emerald-400 transition-colors" onClick={() => navigate('/')}>Home</span>
        <span className="cursor-pointer hover:text-emerald-400 transition-colors" onClick={() => navigate('/stations')}>Stations</span>
        <span className="cursor-pointer hover:text-emerald-400 transition-colors" onClick={() => navigate('/features')}>Features</span>
        <span className="cursor-pointer hover:text-emerald-400 transition-colors" onClick={() => navigate('/contact')}>Contact</span>
      </nav>
      <button className="md:hidden text-slate-300 hover:text-white">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </header>
  );
};

export default Header;
