"use client"

import { motion } from "framer-motion"
import React, { useState } from "react"

export function EnhancedDataVisual({ className }: { className?: string }) {
  const [hoveredBar, setHoveredBar] = useState<number | null>(null);

  // Chart data with realistic values
  const chartData = [
    { x: 10, height: 45, delay: 0.3, label: "Mon" },
    { x: 30, height: 65, delay: 0.4, label: "Tue" },
    { x: 50, height: 35, delay: 0.5, label: "Wed" },
    { x: 70, height: 58, delay: 0.6, label: "Thu" },
    { x: 90, height: 50, delay: 0.7, label: "Fri" }
  ];

  // Line chart points that correspond with the bars
  const linePoints = chartData.map(bar => `${bar.x + 5},${80 - bar.height}`).join(" ");

  return (
    <div className={className}>
      <motion.svg
        viewBox="0 0 110 100"
        fill="none"
        className="w-full h-full"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <defs>
          {/* Enhanced gradients */}
          <linearGradient id="enhancedBarGrad" x1="0%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.7" />
            <stop offset="100%" stopColor="hsl(var(--secondary))" stopOpacity="0.9" />
          </linearGradient>
          
          {/* Glow effect for highlights */}
          <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
          
          {/* Area chart gradient */}
          <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.3" />
            <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity="0" />
          </linearGradient>

          {/* Enhanced grid pattern */}
          <pattern id="smallGrid" width="10" height="10" patternUnits="userSpaceOnUse">
            <path 
              d="M 10 0 L 0 0 0 10" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="0.2" 
              opacity="0.5"
            />
          </pattern>
          <pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse">
            <rect width="100" height="100" fill="url(#smallGrid)" />
            <path 
              d="M 100 0 L 0 0 0 100" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="0.5" 
              opacity="0.8"
            />
          </pattern>
        </defs>

        {/* Enhanced background grid with animation */}
        <motion.rect
          width="100%" 
          height="100%" 
          fill="url(#grid)"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.07 }}
          transition={{ duration: 1 }}
        />
        
        {/* Horizontal guide lines */}
        {[20, 40, 60, 80].map((y) => (
          <motion.line 
            key={`h-${y}`}
            x1="0" 
            y1={y} 
            x2="100" 
            y2={y}
            stroke="currentColor"
            strokeWidth="0.3"
            strokeDasharray="2 2"
            initial={{ opacity: 0, pathLength: 0 }}
            animate={{ opacity: 0.3, pathLength: 1 }}
            transition={{ duration: 1, delay: y * 0.005 }}
          />
        ))}

        {/* Base line */}
        <motion.line
          x1="0" y1="80" x2="100" y2="80"
          stroke="currentColor"
          strokeWidth="0.5"
          initial={{ opacity: 0, pathLength: 0 }}
          animate={{ opacity: 1, pathLength: 1 }}
          transition={{ duration: 0.8 }}
        />

        {/* Y-axis labels */}
        {[0, 25, 50, 75, 100].map((val, i) => (
          <motion.text
            key={`y-label-${i}`}
            x="2"
            y={80 - (val * 0.75) + 3}
            fontSize="3"
            fill="currentColor"
            textAnchor="start"
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.7 }}
            transition={{ duration: 0.5, delay: 0.8 + i * 0.1 }}
          >
            {val}%
          </motion.text>
        ))}

        {/* Data bars with enhanced animations */}
        {chartData.map((bar, i) => (
          <React.Fragment key={i}>
            <motion.rect
              x={bar.x}
              width="10"
              rx="1"
              initial={{ height: 0, y: 80 }}
              animate={{ 
                height: bar.height, 
                y: 80 - bar.height,
                fill: hoveredBar === i 
                  ? "url(#enhancedBarGrad)" 
                  : "url(#enhancedBarGrad)",
                opacity: hoveredBar === null || hoveredBar === i ? 1 : 0.6
              }}
              transition={{ 
                type: "spring", 
                stiffness: 50,
                damping: 15,
                delay: bar.delay,
                opacity: { duration: 0.2 }
              }}
              onMouseEnter={() => setHoveredBar(i)}
              onMouseLeave={() => setHoveredBar(null)}
              style={{ cursor: "pointer" }}
            />

            {/* X-axis labels */}
            <motion.text
              x={bar.x + 5}
              y="85"
              fontSize="3"
              fill="currentColor"
              textAnchor="middle"
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.9 }}
              transition={{ duration: 0.5, delay: bar.delay + 0.3 }}
            >
              {bar.label}
            </motion.text>

            {/* Value labels that appear on hover */}
            <motion.text
              x={bar.x + 5}
              y={78 - bar.height}
              fontSize="3.5"
              fontWeight="bold"
              fill="hsl(var(--primary))"
              textAnchor="middle"
              initial={{ opacity: 0, y: 78 - bar.height + 5 }}
              animate={{ 
                opacity: hoveredBar === i ? 1 : 0,
                y: hoveredBar === i ? 78 - bar.height - 3 : 78 - bar.height + 1
              }}
              transition={{ 
                duration: 0.2,
                type: "spring",
                stiffness: 200
              }}
            >
              {bar.height}
            </motion.text>
          </React.Fragment>
        ))}

        {/* Area under the curve */}
        <motion.path
          d={`M ${chartData[0].x + 5},80 ${linePoints} ${chartData[chartData.length - 1].x + 5},80 Z`}
          fill="url(#areaGradient)"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.2, delay: 1.2 }}
        />

        {/* Smooth line connecting data points */}
        <motion.polyline
          points={linePoints}
          fill="none"
          stroke="hsl(var(--primary))"
          strokeWidth="1"
          strokeLinecap="round"
          strokeLinejoin="round"
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{ 
            duration: 1.5, 
            delay: 0.8, 
            ease: "easeInOut" 
          }}
        />

        {/* Data points on line */}
        {chartData.map((point, i) => (
          <motion.circle
            key={i}
            cx={point.x + 5}
            cy={80 - point.height}
            r="1.5"
            fill="hsl(var(--background))"
            stroke="hsl(var(--primary))"
            strokeWidth="1"
            filter={hoveredBar === i ? "url(#glow)" : ""}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ 
              scale: hoveredBar === i ? 1.5 : 1, 
              opacity: 1 
            }}
            transition={{ 
              type: "spring", 
              delay: 1.1 + i * 0.1,
              scale: { type: "spring", stiffness: 300 }
            }}
            onMouseEnter={() => setHoveredBar(i)}
            onMouseLeave={() => setHoveredBar(null)}
            style={{ cursor: "pointer" }}
          />
        ))}

        {/* Title for the chart */}
        <motion.text
          x="50"
          y="10"
          fontSize="5"
          fontWeight="bold"
          fill="currentColor"
          textAnchor="middle"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 10 }}
          transition={{ duration: 0.7, delay: 0.2 }}
        >
          Weekly News Engagement
        </motion.text>
      </motion.svg>
    </div>
  );
}
