'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export const EmptyStateAnimation = ({ className = '' }: { className?: string }) => {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  if (!mounted) return null;
  
  return (
    <div className={`relative w-48 h-48 mx-auto ${className}`}>
      <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
        <motion.rect 
          x="50" 
          y="40" 
          width="100" 
          height="120" 
          rx="6" 
          fill="#F3F4F6"
          stroke="#D1D5DB"
          strokeWidth="2"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        />
        
        <motion.line 
          x1="70" 
          y1="65" 
          x2="130" 
          y2="65" 
          stroke="#E5E7EB" 
          strokeWidth="4"
          strokeLinecap="round"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        />
        
        <motion.line 
          x1="70" 
          y1="85" 
          x2="130" 
          y2="85" 
          stroke="#E5E7EB" 
          strokeWidth="3"
          strokeLinecap="round"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        />
        
        <motion.line 
          x1="70" 
          y1="105" 
          x2="115" 
          y2="105" 
          stroke="#E5E7EB" 
          strokeWidth="3"
          strokeLinecap="round"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.6, delay: 0.7 }}
        />
        
        <motion.circle 
          cx="100" 
          cy="140" 
          r="12" 
          fill="white"
          stroke="#D1D5DB"
          strokeWidth="2"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 300, delay: 0.9 }}
        />
        
        <motion.path 
          d="M94 140L98 144L106 136" 
          stroke="#D1D5DB"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 0 }}
          transition={{ duration: 0.6, delay: 1.1 }}
        />
        
        <motion.circle 
          cx="100" 
          cy="100" 
          r="50" 
          stroke="#EF4444" 
          strokeWidth="3"
          strokeDasharray="8 8"
          fill="none"
          initial={{ opacity: 0, rotate: 0, scale: 0.8 }}
          animate={{ opacity: 1, rotate: 360, scale: 1 }}
          transition={{ duration: 3, delay: 1, repeat: Infinity, repeatType: "loop" }}
        />
        
        <motion.line 
          x1="70" 
          y1="70" 
          x2="130" 
          y2="130" 
          stroke="#EF4444" 
          strokeWidth="3"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.8, delay: 1.3 }}
        />
        
        <motion.line 
          x1="130" 
          y1="70" 
          x2="70" 
          y2="130" 
          stroke="#EF4444" 
          strokeWidth="3"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.8, delay: 1.6 }}
        />
      </svg>
    </div>
  );
};
