'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export const NewsIconAnimation = ({ className = '' }: { className?: string }) => {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  if (!mounted) return null;
  
  return (
    <div className={`relative w-full h-full max-w-[200px] max-h-[200px] mx-auto ${className}`}>
      <svg 
        viewBox="0 0 200 200" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full"
      >
        <motion.rect 
          x="40" 
          y="40" 
          width="120" 
          height="120" 
          rx="8"
          fill="white"
          stroke="#3B82F6"
          strokeWidth="2"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
        
        <motion.rect 
          x="50" 
          y="55" 
          width="60" 
          height="6" 
          rx="2"
          fill="#3B82F6"
          initial={{ scaleX: 0, originX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
        />
        
        <motion.rect 
          x="50" 
          y="67" 
          width="100" 
          height="4" 
          rx="2"
          fill="#E5E7EB"
          initial={{ scaleX: 0, originX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.6, delay: 0.6, ease: "easeOut" }}
        />
        
        <motion.rect 
          x="50" 
          y="77" 
          width="90" 
          height="4" 
          rx="2"
          fill="#E5E7EB"
          initial={{ scaleX: 0, originX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.6, delay: 0.7, ease: "easeOut" }}
        />
        
        <motion.rect 
          x="50" 
          y="87" 
          width="70" 
          height="4" 
          rx="2"
          fill="#E5E7EB"
          initial={{ scaleX: 0, originX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.6, delay: 0.8, ease: "easeOut" }}
        />
        
        <motion.rect 
          x="50" 
          y="105" 
          width="40" 
          height="10" 
          rx="4"
          fill="#DBEAFE"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1, ease: "easeOut" }}
        />
        
        <motion.rect 
          x="95" 
          y="105" 
          width="40" 
          height="10" 
          rx="4"
          fill="#BFDBFE"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1.2, ease: "easeOut" }}
        />
        
        <motion.circle
          cx="135" 
          cy="55" 
          r="12"
          fill="#DBEAFE"
          stroke="#3B82F6"
          strokeWidth="2"
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ 
            duration: 0.8, 
            delay: 1, 
            type: "spring", 
            stiffness: 200 
          }}
        />
        
        <motion.path
          d="M135 50L135 60M130 55L140 55"
          stroke="#3B82F6"
          strokeWidth="2"
          strokeLinecap="round"
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{ duration: 0.6, delay: 1.4 }}
        />
        
        <motion.path
          d="M50 135C50 135 60 125 70 135C80 145 90 120 100 135C110 150 120 130 130 135C140 140 150 130 150 135"
          stroke="#3B82F6"
          strokeWidth="2"
          strokeLinecap="round"
          fill="none"
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{ duration: 1.5, delay: 1.6 }}
        />
      </svg>
    </div>
  );
};
