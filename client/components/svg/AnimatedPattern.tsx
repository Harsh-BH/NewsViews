'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export const AnimatedPattern = ({ className = '' }: { className?: string }) => {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  if (!mounted) return null;
  
  return (
    <div className={`absolute inset-0 overflow-hidden opacity-[0.03] pointer-events-none ${className}`}>
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 1000 1000"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g>
          <motion.path
            d="M100,300 Q450,100 900,300"
            stroke="#2463EB"
            strokeWidth="1.5"
            fill="transparent"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, ease: "easeInOut" }}
          />
          <motion.path
            d="M100,500 Q450,300 900,500"
            stroke="#3B82F6"
            strokeWidth="1.5"
            fill="transparent"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, delay: 0.5, ease: "easeInOut" }}
          />
          <motion.path
            d="M100,700 Q450,500 900,700"
            stroke="#60A5FA"
            strokeWidth="1.5"
            fill="transparent"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 3, delay: 1, ease: "easeInOut" }}
          />
        </g>
        
        {/* Animated Dots */}
        {[100, 300, 500, 700, 900].map((pos, i) => (
          <motion.circle
            key={i}
            cx={pos}
            cy={700 - i * 100}
            r="4"
            fill="#3B82F6"
            initial={{ scale: 0, opacity: 0 }}
            animate={{ 
              scale: [0, 1.5, 1], 
              opacity: [0, 1, 0.7],
              y: [0, -10, 0],
            }}
            transition={{ 
              repeat: Infinity, 
              duration: 3,
              delay: i * 0.5,
              repeatType: "reverse"
            }}
          />
        ))}
      </svg>
    </div>
  );
};
