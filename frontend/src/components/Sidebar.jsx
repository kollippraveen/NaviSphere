import React, { useState } from 'react';
import { Search, MapPin, Utensils, DoorOpen, LayoutGrid, Info } from 'lucide-react';

const Sidebar = ({ facilities, onSelect, startPoint, endPoint }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");

  const categories = ["All", "Platform", "Food", "Exit", "Utility"];

  const filteredFacilities = facilities.filter(f => {
    const matchesSearch = f.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = activeCategory === "All" || f.category === activeCategory;
    return matchesSearch && matchesCategory;
  });

  const getIcon = (category) => {
    switch (category) {
      case "Food": return <Utensils size={14} />;
      case "Exit": return <DoorOpen size={14} />;
      case "Platform": return <LayoutGrid size={14} />;
      default: return <Info size={14} />;
    }
  };

  return (
    <div className="w-full lg:w-80 bg-slate-800 p-5 rounded-2xl border border-slate-700 shadow-2xl h-fit">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Search size={20} className="text-blue-400" /> Facility Finder
      </h2>
      
      {/* Search Input */}
      <input
        type="text"
        placeholder="Search station..."
        className="w-full p-3 mb-4 bg-slate-900 border border-slate-700 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
        onChange={(e) => setSearchTerm(e.target.value)}
      />

      {/* Category Filter Pills */}
      <div className="flex flex-wrap gap-2 mb-6">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-3 py-1 rounded-full text-xs font-bold transition-all ${
              activeCategory === cat 
              ? "bg-blue-600 text-white" 
              : "bg-slate-700 text-slate-400 hover:bg-slate-600"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Results List */}
      <div className="space-y-2 max-h-[350px] overflow-y-auto pr-2 custom-scrollbar">
        {filteredFacilities.map((f, i) => (
          <button
            key={i}
            onClick={() => onSelect(f)}
            className={`w-full text-left p-3 rounded-xl border transition-all flex items-center justify-between group ${
              startPoint === f.name ? "bg-emerald-500/20 border-emerald-500/50" :
              endPoint === f.name ? "bg-red-500/20 border-red-500/50" :
              "bg-slate-700/30 border-transparent hover:border-slate-500"
            }`}
          >
            <div className="flex items-center gap-3">
              <div className="p-2 bg-slate-800 rounded-lg text-blue-400 group-hover:scale-110 transition-transform">
                {getIcon(f.category)}
              </div>
              <div>
                <p className="text-sm font-semibold">{f.name}</p>
                <p className="text-[10px] text-slate-500 uppercase tracking-widest">{f.category}</p>
              </div>
            </div>
            <MapPin size={14} className="text-slate-600 group-hover:text-blue-400" />
          </button>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;