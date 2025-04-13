"use client"

import { motion } from "framer-motion"
import { useEffect, useState } from "react"

export const NewsFeedAnimation = ({ className }: { className?: string }) => {
  // Create random widths for text lines
  const [widths, setWidths] = useState<number[]>([])
  
  useEffect(() => {
    // Generate random widths for the text lines
    setWidths(
      Array(20).fill(0).map(() => 40 + Math.floor(Math.random() * 50))
    )
  }, [])
  
  return (
    <div className={className}>
      <motion.svg
        width="200"
        height="250"
        viewBox="0 0 200 250"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="feedGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="var(--color-primary)" stopOpacity="0.1" />
            <stop offset="100%" stopColor="var(--color-primary)" stopOpacity="0.05" />
          </linearGradient>
          <mask id="fadeMask">
            <rect x="0" y="0" width="200" height="250" fill="white" />
            <rect x="0" y="0" width="200" height="40" fill="black">
              <animate 
                attributeName="height" 
                values="40;30;20;10;0" 
                dur="0.5s" 
                begin="0s"
                fill="freeze"
              />
            </rect>
            <rect x="0" y="210" width="200" height="0" fill="black">
              <animate 
                attributeName="height" 
                values="0;10;20;30;40" 
                dur="0.5s" 
                begin="0s"
                fill="freeze"
              />
            </rect>
          </mask>
        </defs>
        
        {/* Feed container with gradient background */}
        <motion.rect
          x="0" y="0" width="200" height="250" rx="8"
          fill="url(#feedGradient)"
          stroke="var(--color-border)"
          strokeWidth="2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        />
        
        {/* Feed header */}
        <motion.rect
          x="20" y="15" width="120" height="10" rx="2"
          fill="var(--color-primary)"
          initial={{ opacity: 0, width: 0 }}
          animate={{ opacity: 1, width: 120 }}
          transition={{ delay: 0.3, duration: 0.7 }}
        />
        
        {/* Animated news items */}
        <motion.g
          mask="url(#fadeMask)"
          initial={{ y: 250 }}
          animate={{ y: -250 }}
          transition={{ 
            delay: 1,
            duration: 15, 
            repeat: Infinity,
            repeatType: "loop",
            ease: "linear" 
          }}
        >
          {Array(8).fill(0).map((_, cardIndex) => (
            <g key={cardIndex}>
              {/* Card background */}
              <rect
                x="10" y={50 + cardIndex * 90} width="180" height="80" rx="4"
                fill="var(--color-card)"
                stroke="var(--color-border)"
                strokeWidth="1"
              />
              
              {/* Card content */}
              <rect
                x="20" y={60 + cardIndex * 90} width="100" height="8" rx="2"
                fill="var(--color-text)"
              />
              
              {/* Text lines */}
              {Array(3).fill(0).map((_, lineIndex) => (
                <rect
                  key={lineIndex}
                  x="20" y={73 + lineIndex * 10 + cardIndex * 90} 
                  width={widths[(cardIndex * 3 + lineIndex) % widths.length] || 50} 
                  height="5" rx="1"
                  fill="var(--color-text-muted)"
                />
              ))}
              
              {/* Card button */}
              <rect
                x="20" y={110 + cardIndex * 90} width="60" height="10" rx="5"
                fill="var(--color-primary)"
                fillOpacity="0.7"
              />
            </g>
          ))}
        </motion.g>
        
        {/* Scroll indicator */}
        <motion.circle
          cx="180" cy="125" r="4"
          fill="var(--color-primary)"
          animate={{
            opacity: [0.2, 1, 0.2],
            y: [0, 10, 0]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            repeatType: "reverse"
          }}
        />
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
        }
      `}</style>
    </div>
  )
}
