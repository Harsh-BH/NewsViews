"use client"

import { motion } from "framer-motion"

export const EnhancedNewsAnimation = ({ className }: { className?: string }) => {
  return (
    <div className={className}>
      <motion.svg
        width="300"
        height="300"
        viewBox="0 0 300 300"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Background gradient */}
        <defs>
          <linearGradient id="cardGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="var(--color-primary)" stopOpacity="0.1" />
            <stop offset="100%" stopColor="var(--color-secondary)" stopOpacity="0.05" />
          </linearGradient>
          <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="4" stdDeviation="10" floodOpacity="0.2" />
          </filter>
        </defs>
        
        {/* Mobile device frame */}
        <motion.rect
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          x="70" y="20" width="160" height="260" rx="15"
          fill="var(--color-card)"
          stroke="var(--color-border)"
          strokeWidth="3"
          filter="url(#shadow)"
        />
        
        {/* Screen */}
        <motion.rect
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          x="80" y="40" width="140" height="210" rx="4"
          fill="var(--color-background)"
        />
        
        {/* Logo */}
        <motion.g
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6, duration: 0.5, type: "spring" }}
        >
          <motion.rect
            x="100" y="50" width="100" height="20" rx="4"
            fill="var(--color-primary)"
          />
          <motion.text
            x="150" y="65" 
            textAnchor="middle"
            fill="white"
            fontSize="12"
            fontWeight="bold"
          >
            NewsViews
          </motion.text>
        </motion.g>
        
        {/* Feed items that animate in */}
        {[0, 1, 2].map((i) => (
          <motion.g key={i}
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8 + i * 0.2, duration: 0.5 }}
          >
            <motion.rect
              x="90" y={85 + i * 55} width="120" height="45" rx="4"
              fill="url(#cardGradient)"
              stroke="var(--color-border)"
              strokeWidth="1"
            />
            
            {/* Headline */}
            <motion.rect
              initial={{ width: 0 }}
              animate={{ width: 80 }}
              transition={{ delay: 1.1 + i * 0.2, duration: 0.7, ease: "easeInOut" }}
              x="95" y={92 + i * 55} height="6" rx="2"
              fill="var(--color-text)"
            />
            
            {/* Text lines */}
            <motion.rect
              initial={{ width: 0 }}
              animate={{ width: 110 }}
              transition={{ delay: 1.2 + i * 0.2, duration: 0.6, ease: "easeInOut" }}
              x="95" y={102 + i * 55} height="4" rx="1"
              fill="var(--color-text-muted)"
            />
            <motion.rect
              initial={{ width: 0 }}
              animate={{ width: 90 }}
              transition={{ delay: 1.3 + i * 0.2, duration: 0.6, ease: "easeInOut" }}
              x="95" y={110 + i * 55} height="4" rx="1"
              fill="var(--color-text-muted)"
            />
            <motion.rect
              initial={{ width: 0 }}
              animate={{ width: 75 }}
              transition={{ delay: 1.4 + i * 0.2, duration: 0.6, ease: "easeInOut" }}
              x="95" y={118 + i * 55} height="4" rx="1"
              fill="var(--color-text-muted)"
            />
          </motion.g>
        ))}
        
        {/* Notification dot that pulses */}
        <motion.circle
          initial={{ scale: 0 }}
          animate={{ scale: [0, 1.3, 1] }}
          transition={{ 
            delay: 2.2, 
            duration: 0.5, 
            ease: "easeOut",
            repeat: 2,
            repeatDelay: 3
          }}
          cx="185" cy="55" r="5"
          fill="var(--color-destructive)"
        />
        
        {/* Bottom navigation bar */}
        <motion.rect
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2.0, duration: 0.5 }}
          x="80" y="250" width="140" height="20" rx="0"
          fill="var(--color-card)"
        />
        
        {/* Nav icons */}
        {[0, 1, 2, 3].map((i) => (
          <motion.circle
            key={i}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 2.0 + i * 0.15, duration: 0.3 }}
            cx={105 + i * 30} cy="260" r="4"
            fill={i === 0 ? "var(--color-primary)" : "var(--color-text-muted)"}
          />
        ))}
        
        {/* Scrolling animation */}
        <motion.g
          animate={{ 
            y: [0, -40, -80, -40, 0],
            opacity: [0, 1, 1, 1, 0]
          }}
          transition={{ 
            delay: 2.5, 
            duration: 6,
            times: [0, 0.2, 0.5, 0.8, 1],
            repeat: Infinity,
            repeatDelay: 2
          }}
        >
          <rect
            x="140" y="270" width="20" height="40" rx="10"
            fill="none" stroke="var(--color-primary)" strokeWidth="2"
          />
          <circle
            cx="150" cy="280" r="3"
            fill="var(--color-primary)"
          />
        </motion.g>
      </motion.svg>
      <style jsx>{`
        div {
          --color-primary: hsl(var(--primary));
          --color-secondary: hsl(var(--secondary));
          --color-border: hsl(var(--border));
          --color-card: hsl(var(--card));
          --color-muted: hsl(var(--muted));
          --color-text: hsl(var(--foreground));
          --color-text-muted: hsl(var(--muted-foreground));
          --color-background: hsl(var(--background));
          --color-destructive: hsl(var(--destructive));
        }
      `}</style>
    </div>
  )
}
