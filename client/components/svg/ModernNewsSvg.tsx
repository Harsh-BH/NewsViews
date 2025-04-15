"use client"

import { motion, useAnimationControls, AnimatePresence } from "framer-motion"
import React, { useEffect, useState } from "react"
import { useTheme } from "next-themes"

export function ModernNewsSvg({ className }: { className?: string }) {
  // Theme detection for color adjustments - start with a safe default
  const [mounted, setMounted] = useState(false)
  const { resolvedTheme } = useTheme()
  const isDark = mounted ? resolvedTheme === "dark" : false // Default to light theme during SSR

  // Only access theme after component is mounted
  useEffect(() => {
    setMounted(true)
  }, [])

  // Define theme-aware colors
  const textColor = isDark ? "currentColor" : "#333"
  const borderColor = isDark ? "currentColor" : "#ddd"
  
  // Animation variants for smoother motion
  const phoneVariants = {
    hidden: { y: 30, opacity: 0 },
    visible: { 
      y: 0, 
      opacity: 1,
      transition: { 
        type: "spring", 
        stiffness: 50, 
        damping: 20,
        duration: 0.8 
      }
    }
  };

  const screenVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { 
        delay: 0.3, 
        duration: 0.5,
        ease: "easeOut" 
      }
    }
  };

  const newsCardVariants = {
    hidden: { x: -20, opacity: 0 },
    visible: (custom: number) => ({
      x: 0, 
      opacity: 1,
      transition: { 
        delay: 0.5 + (custom * 0.2),
        type: "spring",
        stiffness: 70,
        damping: 15
      }
    })
  };

  const headlines = [
    "Breaking News",
    "Local Updates",
    "Global Stories",
    "Tech News"
  ];

  // Initialize state with safe default values
  const [currentHeadline, setCurrentHeadline] = useState(0);
  const [weatherState, setWeatherState] = useState("sunny");
  const [liked, setLiked] = useState(false);
  
  // Setup animation controls
  const videoPlayControls = useAnimationControls();
  const likeControls = useAnimationControls();

  // Client-side only animations - only run after component mounts
  useEffect(() => {
    if (!mounted) return;
    
    // Rotate through headlines
    const headlineInterval = setInterval(() => {
      setCurrentHeadline((prev) => (prev + 1) % headlines.length);
    }, 3000);
    
    // Cycle through weather states
    const weatherInterval = setInterval(() => {
      setWeatherState(prev => {
        switch(prev) {
          case "sunny": return "cloudy";
          case "cloudy": return "rainy";
          case "rainy": return "sunny";
          default: return "sunny";
        }
      });
    }, 5000);
    
    // Video play animation
    const playVideo = async () => {
      await videoPlayControls.start({ scale: 1.2, opacity: 0, transition: { duration: 0.3 } });
      await videoPlayControls.set({ scale: 0, opacity: 1 });
      await videoPlayControls.start({ scale: 1, opacity: 1, transition: { duration: 0.2 } });
    };
    
    const videoTimer = setTimeout(playVideo, 4000);
    const videoInterval = setInterval(playVideo, 8000);
    
    // Like button animation
    const toggleLike = async () => {
      await likeControls.start({ scale: 1.3, transition: { duration: 0.2 } });
      await likeControls.start({ scale: 1, transition: { duration: 0.2 } });
      setLiked(prev => !prev);
    };
    
    const likeTimer = setTimeout(toggleLike, 3000);
    const likeInterval = setInterval(toggleLike, 7000);
    
    // Clear all timers on unmount
    return () => {
      clearInterval(headlineInterval);
      clearInterval(weatherInterval);
      clearTimeout(videoTimer);
      clearInterval(videoInterval);
      clearTimeout(likeTimer);
      clearInterval(likeInterval);
    };
  }, [mounted, videoPlayControls, likeControls, headlines.length]);



  // If not mounted yet, render a placeholder version with minimal animations
  if (!mounted) {
    return (
      <div className={className}>
        <svg viewBox="0 0 360 360" fill="none" className="w-full h-full">
          {/* Simple static phone - minimal but consistent between server/client */}
          <rect
            x="80" y="20" width="200" height="320" rx="20"
            fill="#2a2a2a"
            stroke="#000000"
            strokeOpacity="0.2"
            strokeWidth="1.5"
          />
          <rect
            x="90" y="40" width="180" height="280" rx="10"
            fill="#ffffff"
          />
          <rect
            x="90" y="40" width="180" height="20" rx="10" ry="0"
            fill="hsl(var(--primary))"
            fillOpacity="0.8"
          />
        </svg>
      </div>
    );
  }

  // Full interactive component - only rendered client-side
  return (
    <div className={className}>
      <svg viewBox="0 0 360 360" fill="none" className="w-full h-full">
        <defs>
          {/* Phone frame gradient - always dark regardless of theme */}
          <linearGradient id="phoneFrameGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#2a2a2a" />
            <stop offset="100%" stopColor="#111111" stopOpacity="0.9" />
          </linearGradient>

          {/* Phone button gradient - visible on dark frame */}
          <linearGradient id="phoneButtonGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#444444" />
            <stop offset="100%" stopColor="#333333" />
          </linearGradient>

          {/* Screen gradient - theme-aware */}
          <linearGradient id="screenGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={isDark ? "hsl(var(--background))" : "#ffffff"} />
            <stop offset="100%" stopColor={isDark ? "hsl(var(--muted))" : "#f5f5f5"} stopOpacity="0.3" />
          </linearGradient>

          {/* Enhanced drop shadow for better visibility in light mode */}
          <filter id="phoneDropShadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="10" stdDeviation="15" floodOpacity="0.3" />
          </filter>

          {/* News card gradients - theme-aware */}
          <linearGradient id="cardGradient1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={isDark ? "0.05" : "0.1"} />
            <stop offset="100%" stopColor="hsl(var(--secondary))" stopOpacity={isDark ? "0.1" : "0.15"} />
          </linearGradient>

          <linearGradient id="cardGradient2" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(var(--secondary))" stopOpacity={isDark ? "0.1" : "0.15"} />
            <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity={isDark ? "0.05" : "0.1"} />
          </linearGradient>

          {/* Weather widget gradient - theme-aware */}
          <linearGradient id="weatherGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={isDark ? "0.1" : "0.15"} />
            <stop offset="100%" stopColor="hsl(var(--secondary))" stopOpacity={isDark ? "0.1" : "0.15"} />
          </linearGradient>
          
          {/* Video player gradient */}
          <linearGradient id="videoGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={isDark ? "#444" : "#777"} />
            <stop offset="100%" stopColor={isDark ? "#111" : "#444"} />
          </linearGradient>

          {/* Drop shadow - adjusted for light mode */}
          <filter id="phoneDropShadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="10" stdDeviation={isDark ? "15" : "7"} floodOpacity={isDark ? "0.2" : "0.08"} />
          </filter>

          {/* Notification dot glow - theme-aware */}
          <filter id="notificationGlow" x="-100%" y="-100%" width="300%" height="300%">
            <feGaussianBlur stdDeviation={isDark ? "2" : "1.5"} result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>

          {/* Like button glow - theme-aware */}
          <filter id="heartGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="1" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>

          {/* News app header gradient */}
          <linearGradient id="headerGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(var(--primary))" />
            <stop offset="100%" stopColor="hsl(var(--secondary))" />
          </linearGradient>
          
          {/* News ticker gradient */}
          <linearGradient id="tickerGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(var(--secondary))" stopOpacity="0.7" />
            <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity="0.7" />
          </linearGradient>
          
          {/* Video play button with theme-aware colors */}
          <radialGradient id="playGradient" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
            <stop offset="0%" stopColor="hsl(var(--secondary))" stopOpacity="1" />
            <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity="1" />
          </radialGradient>
          
          {/* Image placeholder gradients - theme-aware */}
          <linearGradient id="imagePlaceholder1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={isDark ? "0.2" : "0.3"} />
            <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity={isDark ? "0.1" : "0.15"} />
          </linearGradient>

          <linearGradient id="imagePlaceholder2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="hsl(var(--secondary))" stopOpacity={isDark ? "0.2" : "0.3"} />
            <stop offset="100%" stopColor="hsl(var(--secondary))" stopOpacity={isDark ? "0.1" : "0.15"} />
          </linearGradient>
        </defs>

        {/* Phone frame with shadow - always dark */}
        <motion.rect
          variants={phoneVariants}
          initial="hidden"
          animate="visible"
          x="80" y="20" width="200" height="320" rx="20"
          fill="url(#phoneFrameGradient)"
          stroke="#000000"
          strokeOpacity="0.2"
          strokeWidth="1.5"
          filter="url(#phoneDropShadow)"
        />

        {/* Phone buttons - visible on dark frame */}
        <motion.rect
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.8 }}
          transition={{ delay: 0.9 }}
          x="75" y="100" width="2" height="40" rx="1"
          fill="url(#phoneButtonGradient)"
        />
        <motion.rect
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.8 }}
          transition={{ delay: 0.9 }}
          x="75" y="150" width="2" height="60" rx="1"
          fill="url(#phoneButtonGradient)"
        />
        <motion.rect
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.8 }}
          transition={{ delay: 0.9 }}
          x="283" y="120" width="2" height="30" rx="1" 
          fill="url(#phoneButtonGradient)"
        />

        {/* Screen bezel/edge - thin border around screen */}
        <motion.rect
          variants={screenVariants}
          initial="hidden"
          animate="visible"
          x="89" y="39" width="182" height="282" rx="11"
          fill="#000000"
          fillOpacity="0.8"
        />

        {/* Screen */}
        <motion.rect
          variants={screenVariants}
          initial="hidden"
          animate="visible"
          x="90" y="40" width="180" height="280" rx="10"
          fill="url(#screenGradient)"
        />

        {/* App Status bar */}
        <motion.rect
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.9 }}
          transition={{ delay: 0.6 }}
          x="90" y="40" width="180" height="20" rx="10" ry="0"
          fill="url(#headerGradient)"
          fillOpacity="0.8"
        />
        <motion.circle
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.7, type: "spring", stiffness: 200 }}
          cx="100" cy="50" r="4"
          fill="white"
        />
        <motion.rect
          initial={{ width: 0 }}
          animate={{ width: 20 }}
          transition={{ delay: 0.7, duration: 0.4 }}
          x="240" y="48" height="4" rx="2"
          fill="white"
        />

        {/* App header with logo */}
        <motion.rect
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          x="90" y="60" width="180" height="40" 
          fill="url(#headerGradient)"
          fillOpacity="0.1"
        />

        <motion.text
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.9 }}
          x="180" y="85"
          textAnchor="middle"
          fontSize="16"
          fontWeight="bold"
          fill={textColor}
        >
          NewsViews
        </motion.text>
        
        {/* Animated headlines */}
        <g>
          <rect 
            x="100" y="95" width="160" height="20" 
            fill="url(#tickerGradient)"
            rx="4"
          />
          <AnimatePresence mode="wait">
            <motion.text
              key={currentHeadline}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.4 }}
              x="180" y="108"
              textAnchor="middle"
              fontSize="10"
              fontWeight="bold"
              fill="white"
            >
              {headlines[currentHeadline]}
            </motion.text>
          </AnimatePresence>
        </g>

        {/* First news card with video player */}
        <motion.g
          variants={newsCardVariants}
          initial="hidden"
          animate="visible"
          custom={0}
        >
          <rect
            x="100" y="120" width="160" height="75" rx="6"
            fill="url(#cardGradient1)"
            stroke={borderColor}
            strokeOpacity="0.1"
            strokeWidth="1"
          />
          
          {/* Video player */}
          <rect
            x="110" y="130" width="60" height="40" rx="3"
            fill="url(#videoGradient)"
          />
          <motion.circle
            animate={videoPlayControls}
            cx="140" cy="150" r="8"
            fill="url(#playGradient)"
          />
          <motion.path
            d="M138,147 L138,153 L144,150 Z"
            fill="white"
            animate={videoPlayControls}
          />
          
          <rect
            x="180" y="130" width="70" height="8" rx="2"
            fill={textColor}
            fillOpacity="0.7"
          />
          {[0, 1, 2].map((i) => (
            <rect
              key={i}
              x="180" y={143 + i * 8} width={70 - i * 15} height="5" rx="2"
              fill={textColor}
              fillOpacity={isDark ? "0.4" : "0.5"}
            />
          ))}
        </motion.g>

        {/* Weather widget with animated elements */}
        <motion.g
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2, duration: 0.6 }}
        >
          <rect
            x="100" y="200" width="80" height="40" rx="6"
            fill="url(#weatherGradient)"
            stroke={borderColor}
            strokeOpacity="0.1"
            strokeWidth="1"
          />
          
          <AnimatePresence mode="wait">
            {weatherState === "sunny" && (
              <motion.g
                key="sunny"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.4 }}
              >
                <motion.circle
                  cx="120" cy="220" r="8"
                  fill="hsl(45, 100%, 60%)"
                  animate={{ scale: [1, 1.1, 1] }}
                  transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
                />
                <motion.g
                  animate={{ rotate: [0, 360] }}
                  transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
                  style={{ originX: "120px", originY: "220px" }}
                >
                  {[0, 45, 90, 135, 180, 225, 270, 315].map((angle) => (
                    <motion.line
                      key={angle}
                      x1="120"
                      y1="220"
                      x2={120 + Math.cos(angle * Math.PI / 180) * 12}
                      y2={220 + Math.sin(angle * Math.PI / 180) * 12}
                      stroke="hsl(45, 100%, 60%)"
                      strokeWidth="1"
                      strokeDasharray="0 8 3"
                    />
                  ))}
                </motion.g>
              </motion.g>
            )}
            
            {weatherState === "cloudy" && (
              <motion.g
                key="cloudy"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.4 }}
              >
                <motion.path
                  d="M112,220 Q116,215 122,216 Q124,213 128,214 Q132,214 133,218 Q136,219 137,223 Q135,225 130,225 Q128,228 124,227 Q121,229 117,226 Q114,227 113,224 Q110,222 112,220 Z"
                  fill={isDark ? "lightgray" : "#aaaaaa"}
                  animate={{ x: [-1, 1, -1] }}
                  transition={{ repeat: Infinity, duration: 6, ease: "easeInOut" }}
                />
              </motion.g>
            )}
            
            {weatherState === "rainy" && (
              <motion.g
                key="rainy"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.4 }}
              >
                <path
                  d="M112,218 Q116,213 122,214 Q124,211 128,212 Q132,212 133,216 Q136,217 137,221 Q135,223 130,223 Q128,226 124,225 Q121,227 117,224 Q114,225 113,222 Q110,220 112,218 Z"
                  fill={isDark ? "gray" : "#888888"}
                />
                {[1, 2, 3, 4].map((i) => (
                  <motion.line
                    key={i}
                    x1={113 + i * 5}
                    y1="223"
                    x2={113 + i * 5}
                    y2="228"
                    stroke={isDark ? "lightblue" : "#64a9e6"}
                    strokeWidth="1"
                    animate={{
                      y1: ["223%", "223%", "228%"],
                      y2: ["223%", "228%", "233%"],
                      opacity: [0, 1, 0]
                    }}
                    transition={{
                      duration: 0.8,
                      delay: i * 0.2,
                      repeat: Infinity,
                      repeatDelay: 0.5,
                    }}
                  />
                ))}
              </motion.g>
            )}
          </AnimatePresence>
          
          <text
            x="150" y="217"
            textAnchor="middle"
            fontSize="8"
            fontWeight="bold"
            fill={textColor}
          >
            64°F
          </text>
          <text
            x="150" y="230"
            textAnchor="middle"
            fontSize="6"
            fill={textColor}
            opacity="0.7"
          >
            New York
          </text>
        </motion.g>
        
        {/* Share and like buttons */}
        <motion.g
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.4, duration: 0.5 }}
        >
          <rect
            x="190" y="200" width="70" height="40" rx="6"
            fill="url(#cardGradient2)"
            stroke={borderColor}
            strokeOpacity="0.1"
            strokeWidth="1"
          />
          
          <motion.path
            d="M210,220 Q214,215 218,220 Q222,215 226,220 L218,228 Z"
            fill={liked ? "hsl(0, 80%, 60%)" : "none"}
            stroke={liked ? "hsl(0, 80%, 60%)" : textColor}
            strokeWidth="1.5"
            animate={likeControls}
            filter={liked ? "url(#heartGlow)" : "none"}
          />
          
          <text
            x="218" y="235"
            textAnchor="middle"
            fontSize="6"
            fill={textColor}
          >
            {liked ? "You liked this" : "Like"}
          </text>
          
          <motion.path
            d="M240,216 C243,216 246,218 246,222 C246,228 240,230 240,230 C240,230 234,228 234,222 C234,218 237,216 240,216 Z"
            fill="none"
            stroke={textColor}
            strokeWidth="1.5"
            whileHover={{ scale: 1.1 }}
          />
          <motion.circle cx="240" cy="219" r="1" fill={textColor} />
          <text
            x="240" y="235"
            textAnchor="middle"
            fontSize="6"
            fill={textColor}
          >
            Share
          </text>
        </motion.g>

        {/* News feed items */}
        <motion.g
          variants={newsCardVariants}
          initial="hidden"
          animate="visible"
          custom={1}
        >
          <rect
            x="100" y="245" width="160" height="65" rx="6"
            fill="url(#cardGradient2)"
            stroke={borderColor}
            strokeOpacity="0.1"
            strokeWidth="1"
          />
          <rect
            x="110" y="255" width="40" height="40" rx="3"
            fill="url(#imagePlaceholder2)"
          />
          <rect
            x="155" y="255" width="95" height="8" rx="2"
            fill={textColor}
            fillOpacity="0.7"
          />
          {[0, 1, 2].map((i) => (
            <rect
              key={i}
              x="155" y={268 + i * 8} width={95 - i * 15} height="5" rx="2"
              fill={textColor}
              fillOpacity={isDark ? "0.4" : "0.5"}
            />
          ))}
        </motion.g>

        {/* Bottom navigation bar */}
        <motion.rect
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.8, duration: 0.5 }}
          x="90" y="310" width="180" height="10"
          fill={textColor}
          fillOpacity={isDark ? "0.1" : "0.15"}
          rx="0"
        />

        {/* Navigation icons */}
        {[0, 1, 2, 3].map((i) => (
          <motion.circle
            key={i}
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ 
              delay: 1.9 + i * 0.1, 
              type: "spring", 
              stiffness: 300
            }}
            cx={120 + i * 40} cy="315" r="3"
            fill={i === 1 ? "hsl(var(--primary))" : textColor}
            fillOpacity={i === 1 ? 0.8 : (isDark ? 0.4 : 0.6)}
          />
        ))}

        {/* Notification animation */}
        <motion.circle
          initial={{ opacity: 0, scale: 0 }}
          animate={{ 
            opacity: [0, 1, 0.8],
            scale: [0, 1.2, 1]
          }}
          transition={{ 
            delay: 2.2,
            duration: 0.7,
            times: [0, 0.7, 1],
            repeatDelay: 5,
            repeat: Infinity
          }}
          cx="250" cy="70" r="5"
          fill="hsl(var(--destructive))"
          filter="url(#notificationGlow)"
        />
        
        {/* Random notification popup */}
        <motion.g
          initial={{ opacity: 0, y: -10, scale: 0.9 }}
          animate={{ 
            opacity: [0, 1, 1, 0],
            y: [-10, 0, 0, -10],
            scale: [0.9, 1, 1, 0.9]
          }}
          transition={{ 
            duration: 4,
            times: [0, 0.1, 0.9, 1],
            repeat: Infinity,
            repeatDelay: 10,
            delay: 5
          }}
        >
          <rect
            x="110" y="70" width="140" height="25" rx="4"
            fill="hsl(var(--primary))"
            opacity="0.9"
          />
          <text
            x="180" y="82"
            textAnchor="middle"
            fontSize="8"
            fontWeight="bold"
            fill="white"
          >
            New story from your area
          </text>
          <text
            x="180" y="92"
            textAnchor="middle"
            fontSize="6"
            fill="white"
            opacity="0.8"
          >
            Tap to read now
          </text>
        </motion.g>
      </svg>
    </div>
  );
}
