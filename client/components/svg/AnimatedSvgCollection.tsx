"use client"

// Export the new ModernNewsSvg as the default NewsSvg
export { ModernNewsSvg as NewsSvg } from './ModernNewsSvg'

import { motion } from "framer-motion"
import React, { useEffect, useState } from "react"
import { useTheme } from "next-themes"

// Shared hook for theme detection with SSR support
function useThemeDetection() {
  const [mounted, setMounted] = useState(false);
  const { resolvedTheme } = useTheme();
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  // Default to light theme for SSR
  return {
    isDark: mounted ? resolvedTheme === "dark" : false,
    mounted
  };
}

// Contact/Message SVG Animation with improved smoothness
export function MessageSvg({ className }: { className?: string }) {
  const { isDark, mounted } = useThemeDetection();
  
  // Simple version for SSR
  if (!mounted) {
    return (
      <div className={className}>
        <svg viewBox="0 0 100 100" fill="none" className="w-full h-full">
          <rect 
            x="20" y="20" width="60" height="40" rx="2"
            stroke="currentColor" strokeWidth="2" strokeLinecap="round"
            fill="none"
          />
        </svg>
      </div>
    );
  }

  // Rest of the component with animations for client-side
  const pathVariants = {
    hidden: { pathLength: 0, opacity: 0 },
    visible: (delay: number) => ({
      pathLength: 1, 
      opacity: 1,
      transition: { 
        pathLength: { 
          type: "spring",
          duration: 1.5, 
          bounce: 0, 
          delay 
        },
        opacity: { duration: 0.6, delay }
      }
    })
  };

  return (
    <div className={className}>
      <svg viewBox="0 0 100 100" fill="none" className="w-full h-full">
        <defs>
          <linearGradient id="messageGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={isDark ? "0.3" : "0.4"} />
            <stop offset="100%" stopColor="hsl(var(--secondary))" stopOpacity={isDark ? "0.1" : "0.2"} />
          </linearGradient>
        </defs>
        
        <motion.rect
          variants={pathVariants}
          custom={0}
          initial="hidden"
          animate="visible"
          x="20" y="20" width="60" height="40" rx="2"
          stroke="currentColor" strokeWidth="2" strokeLinecap="round"
          fill="url(#messageGradient)"
        />
        <motion.path
          variants={pathVariants}
          custom={0.3}
          initial="hidden"
          animate="visible"
          d="M20 25L50 45L80 25"
          stroke="currentColor" strokeWidth="2" strokeLinecap="round"
        />
        <motion.path
          variants={pathVariants}
          custom={0.6}
          initial="hidden"
          animate="visible"
          d="M40 70L40 80L60 80L60 70"
          stroke="currentColor" strokeWidth="2" strokeLinecap="round"
        />
        <motion.circle
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ 
            type: "spring",
            stiffness: 200, 
            damping: 15,
            delay: 0.9 
          }}
          cx="50" cy="80" r="5"
          stroke="currentColor" strokeWidth="2"
          fill="hsl(var(--primary))"
        />
      </svg>
    </div>
  );
}

// Animated Circuit/Network Pattern with smoother animations
export function NetworkSvg({ className, delay = 0 }: { className?: string; delay?: number }) {
  const { isDark, mounted } = useThemeDetection();
  
  // Simple version for SSR
  if (!mounted) {
    return (
      <div className={className}>
        <svg viewBox="0 0 100 100" fill="none" className="w-full h-full">
          <path 
            d="M10,50 C30,20 70,80 90,50"
            stroke="currentColor"
            strokeWidth="0.5"
            fill="none"
          />
        </svg>
      </div>
    );
  }

  // Rest of the component with animations for client-side
  const pathVariants = {
    hidden: { pathLength: 0, opacity: 0 },
    visible: (customDelay: number) => ({
      pathLength: 1,
      opacity: [0, isDark ? 0.8 : 1, isDark ? 0.5 : 0.7],
      transition: { 
        pathLength: { duration: 2.5, delay: delay + customDelay, ease: "easeOut" },
        opacity: { 
          duration: 2, 
          delay: delay + customDelay, 
          times: [0, 0.4, 1],
          repeat: Infinity, 
          repeatType: "reverse"
        }
      }
    })
  };

  const nodeVariants = {
    hidden: { scale: 0, opacity: 0 },
    visible: (customDelay: number) => ({
      scale: [0, 1, 0.8],
      opacity: [0, 1, isDark ? 0.5 : 0.7],
      transition: { 
        duration: 3, 
        delay: delay + customDelay, 
        times: [0, 0.4, 1],
        ease: "easeOut",
        repeat: Infinity, 
        repeatType: "reverse"
      }
    })
  };

  return (
    <div className={className}>
      <svg viewBox="0 0 100 100" fill="none" className="w-full h-full">
        {/* Connection lines with smoother animations */}
        <motion.path
          variants={pathVariants}
          initial="hidden"
          animate="visible"
          custom={0.2}
          d="M10,50 C30,20 70,80 90,50"
          stroke="currentColor"
          strokeWidth={isDark ? "0.5" : "0.7"}
          strokeDasharray="1 3"
        />
        
        <motion.path
          variants={pathVariants}
          initial="hidden"
          animate="visible"
          custom={0.5}
          d="M20,20 C40,40 60,10 80,30"
          stroke="currentColor"
          strokeWidth={isDark ? "0.5" : "0.7"}
          strokeDasharray="1 3"
        />
        
        <motion.path
          variants={pathVariants}
          initial="hidden"
          animate="visible"
          custom={0.8}
          d="M20,80 C40,60 70,90 90,70"
          stroke="currentColor"
          strokeWidth={isDark ? "0.5" : "0.7"}
          strokeDasharray="1 3"
        />
        
        {/* Nodes with improved animations */}
        {[
          {x: 10, y: 50, delay: 0}, 
          {x: 20, y: 20, delay: 0.3}, 
          {x: 20, y: 80, delay: 0.6}, 
          {x: 90, y: 50, delay: 0.2}, 
          {x: 80, y: 30, delay: 0.5}, 
          {x: 90, y: 70, delay: 0.8}
        ].map((node, i) => (
          <motion.circle
            key={i}
            variants={nodeVariants}
            initial="hidden"
            animate="visible"
            custom={node.delay}
            cx={node.x} 
            cy={node.y} 
            r="1.5"
            fill="hsl(var(--primary))"
          />
        ))}
      </svg>
    </div>
  );
}

// Floating Bubbles with improved gradient and smooth animations
export function BubblesSvg({ className }: { className?: string }) {
  const { isDark, mounted } = useThemeDetection();
  
  // Simple version for SSR
  if (!mounted) {
    return (
      <div className={className}>
        <svg viewBox="0 0 100 100" fill="none" className="w-full h-full">
          <circle 
            cx="30" cy="30" r="15"
            fill="none"
            stroke="currentColor"
            strokeWidth="0.5"
          />
        </svg>
      </div>
    );
  }

  // Rest of the component with animations for client-side
  const bubbleVariants = {
    hidden: { opacity: 0, y: 0 },
    visible: (custom: { duration: number; delay: number }) => ({
      opacity: isDark ? [0.3, 0.6, 0.3] : [0.5, 0.8, 0.5],
      y: [-5, 5, -5],
      scale: [1, 1.05, 1],
      transition: { 
        duration: custom.duration,
        delay: custom.delay,
        repeat: Infinity,
        ease: "easeInOut"
      }
    })
  };

  return (
    <div className={className}>
      <svg viewBox="0 0 100 100" fill="none" className="w-full h-full">
        <defs>
          <radialGradient id="bubbleGrad1" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
            <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={isDark ? "0.4" : "0.5"} />
            <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity="0" />
          </radialGradient>
          <radialGradient id="bubbleGrad2" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
            <stop offset="0%" stopColor="hsl(var(--secondary))" stopOpacity={isDark ? "0.3" : "0.4"} />
            <stop offset="100%" stopColor="hsl(var(--secondary))" stopOpacity="0" />
          </radialGradient>
        </defs>
        
        {[
          { x: 30, y: 30, r: 15, grad: "url(#bubbleGrad1)", delay: 0, duration: 15 },
          { x: 70, y: 40, r: 10, grad: "url(#bubbleGrad2)", delay: 2, duration: 12 },
          { x: 40, y: 70, r: 12, grad: "url(#bubbleGrad1)", delay: 4, duration: 18 },
          { x: 80, y: 80, r: 8, grad: "url(#bubbleGrad2)", delay: 1, duration: 20 },
          { x: 20, y: 60, r: 6, grad: "url(#bubbleGrad1)", delay: 3, duration: 14 }
        ].map((bubble, i) => (
          <motion.circle
            key={i}
            variants={bubbleVariants}
            initial="hidden"
            animate="visible"
            custom={bubble}
            cx={bubble.x}
            cy={bubble.y}
            r={bubble.r}
            fill={bubble.grad}
          />
        ))}
      </svg>
    </div>
  );
}

// Animated News Icons with smoother animations
export function NewsIconsSvg({ className }: { className?: string }) {
  const { isDark, mounted } = useThemeDetection();
  
  // Simple version for SSR
  if (!mounted) {
    return (
      <div className={className}>
        <svg viewBox="0 0 100 100" fill="none" className="w-full h-full">
          <path 
            d="M20,20 h40 v60 h-40 z"
            stroke="currentColor" 
            strokeWidth="2"
            fill="none"
          />
        </svg>
      </div>
    );
  }

  // Rest of the component with animations for client-side
  const pathVariants = {
    hidden: { pathLength: 0, opacity: 0 },
    visible: (delay: number) => ({
      pathLength: 1, 
      opacity: 1,
      transition: { 
        pathLength: { 
          type: "spring",
          duration: 1.5, 
          bounce: 0, 
          delay 
        },
        opacity: { duration: 0.6, delay }
      }
    })
  };

  return (
    <div className={className}>
      <svg viewBox="0 0 100 100" fill="none" className="w-full h-full">
        {/* News Paper Icon with smoother animations */}
        <motion.path
          variants={pathVariants}
          initial="hidden"
          animate="visible"
          custom={0.2}
          d="M20,20 h40 v60 h-40 z"
          stroke="currentColor" 
          strokeWidth={isDark ? "2" : "2.5"}
          strokeLinecap="round"
          fill="none"
        />
        
        <motion.path
          variants={pathVariants}
          initial="hidden"
          animate="visible"
          custom={0.5}
          d="M60,20 v10 h10 v50 h-10"
          stroke="currentColor" 
          strokeWidth={isDark ? "2" : "2.5"}
          strokeLinecap="round"
          fill="none"
        />
        
        <motion.path
          variants={pathVariants}
          initial="hidden"
          animate="visible"
          custom={0.7}
          d="M30,30 h20 M30,40 h30 M30,45 h30 M30,50 h20 M30,55 h30 M30,60 h25"
          stroke="hsl(var(--primary))" 
          strokeWidth="2" 
          strokeLinecap="round"
          strokeDasharray="0 5"
        />
        
        {/* Reading Glasses with spring animation */}
        <motion.circle
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ 
            type: "spring",
            stiffness: 150, 
            damping: 15,
            delay: 1 
          }}
          cx="75" cy="70" r="8"
          stroke="hsl(var(--secondary))"
          strokeWidth="2"
          fill="none"
        />
        
        <motion.circle
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ 
            type: "spring",
            stiffness: 150, 
            damping: 15,
            delay: 1.1 
          }}
          cx="90" cy="70" r="8"
          stroke="hsl(var(--secondary))"
          strokeWidth="2"
          fill="none"
        />
        
        <motion.path
          variants={pathVariants}
          initial="hidden"
          animate="visible"
          custom={1.2}
          d="M83,70 h2"
          stroke="hsl(var(--secondary))"
          strokeWidth="2"
        />
        
        <motion.path
          variants={pathVariants}
          initial="hidden"
          animate="visible"
          custom={1.3}
          d="M72,62 c-3,-3 -8,-2 -8,2"
          stroke="hsl(var(--secondary))"
          strokeWidth="2"
        />
        
        {/* Notification badge with pulse animation */}
        <motion.circle
          initial={{ scale: 0 }}
          animate={{ 
            scale: [0, 1.2, 1],
            opacity: [0, 1, 0.8]
          }}
          transition={{ 
            times: [0, 0.7, 1],
            duration: 0.8, 
            delay: 1.4,
            repeat: Infinity,
            repeatDelay: 3
          }}
          cx="70" cy="30" r="10"
          fill={isDark ? "hsl(var(--primary))" : "hsl(var(--primary))"}
          fillOpacity={isDark ? "1" : "0.9"}
        />
        
        <motion.text
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 1.6 }}
          x="70" y="33"
          textAnchor="middle"
          fontSize="10"
          fill="white"
          fontWeight="bold"
        >
          3
        </motion.text>
      </svg>
    </div>
  );
}
