"use client"

import { motion } from "framer-motion"

export const NewsAnimation = ({ className }: { className?: string }) => {
  return (
    <div className={className}>
      <motion.svg
        width="240"
        height="240"
        viewBox="0 0 240 240"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <motion.rect
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          x="40" y="40" width="160" height="180" rx="8"
          fill="var(--color-card)"
          stroke="var(--color-border)"
          strokeWidth="2"
        />
        
        {/* Paper stack effect */}
        <motion.rect
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 0.6, x: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          x="30" y="30" width="160" height="180" rx="8"
          fill="var(--color-muted)"
          stroke="var(--color-border)"
          strokeWidth="2"
        />
        
        {/* Headline */}
        <motion.rect
          initial={{ width: 0 }}
          animate={{ width: 120 }}
          transition={{ delay: 0.7, duration: 0.7, ease: "easeInOut" }}
          x="60" y="60" height="12" rx="2"
          fill="var(--color-primary)"
        />
        
        {/* Text lines */}
        {[0, 1, 2, 3, 4].map((i) => (
          <motion.rect
            key={i}
            initial={{ width: 0 }}
            animate={{ width: 120 - (i % 2 === 0 ? 30 : 0) }}
            transition={{ delay: 0.8 + i * 0.1, duration: 0.7, ease: "easeInOut" }}
            x="60" y={90 + i * 16} height="6" rx="2"
            fill="var(--color-text-muted)"
          />
        ))}
        
        {/* Notification circle */}
        <motion.circle
          initial={{ scale: 0 }}
          animate={{ scale: [0, 1.2, 1] }}
          transition={{ delay: 1.5, duration: 0.5, ease: "easeInOut" }}
          cx="170" cy="60" r="12"
          fill="var(--color-primary)"
        />
        
        {/* Animated wave on bottom */}
        <motion.path
          initial={{ pathLength: 0, pathOffset: 1 }}
          animate={{ pathLength: 1, pathOffset: 0 }}
          transition={{ delay: 1, duration: 1.5, ease: "easeInOut" }}
          d="M40 180 C80 160, 120 200, 160 180, 200 160"
          stroke="var(--color-primary)"
          strokeWidth="2"
          fill="none"
        />
      </motion.svg>
      <style jsx>{`
        div {
          --color-primary: hsl(var(--primary));
          --color-border: hsl(var(--border));
          --color-card: hsl(var(--card));
          --color-muted: hsl(var(--muted));
          --color-text-muted: hsl(var(--muted-foreground));
        }
      `}</style>
    </div>
  )
}
