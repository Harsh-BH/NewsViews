"use client"

import { motion, MotionValue } from "framer-motion"
import { useEffect, useState } from "react"

interface StarProps {
  top: string;
  left: string;
  scale: number;
  animY: number;
  duration: number;
}

export default function AnimatedStars({ starsOpacity }: { starsOpacity: MotionValue<number> }) {
  const [mounted, setMounted] = useState(false);
  const [stars, setStars] = useState<StarProps[]>([]);
  
  // Generate stars only after component mounts
  useEffect(() => {
    setMounted(true);
    
    // Generate stars with consistent seed to avoid hydration mismatch
    setStars(Array(20).fill(0).map((_, i) => ({
      top: `${(i * 5) % 100}%`,
      left: `${(i * 7) % 100}%`,
      scale: (i % 5 + 1) * 0.5,
      animY: -((i % 10) + 5),
      duration: (i % 5) + 3
    })));
  }, []);

  if (!mounted) return <div className="absolute inset-0 pointer-events-none overflow-hidden" />;

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      <motion.div style={{ opacity: starsOpacity }}>
        {stars.map((star, i) => (
          <motion.div 
            key={i}
            className="absolute h-1 w-1 rounded-full bg-primary/20 dark:bg-primary/40"
            style={{
              top: star.top,
              left: star.left,
              scale: star.scale
            }}
            animate={{
              y: [0, star.animY],
              opacity: [0.7, 1, 0.7],
            }}
            transition={{
              duration: star.duration,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        ))}
      </motion.div>
    </div>
  );
}
