"use client"

import { motion } from "framer-motion"

export const NotificationBellAnimation = ({ className }: { className?: string }) => {
  return (
    <div className={className}>
      <motion.svg
        width="40" 
        height="40" 
        viewBox="0 0 40 40" 
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Bell body */}
        <motion.path
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1, delay: 0.2 }}
          d="M16 8C16 6.89543 16.8954 6 18 6H22C23.1046 6 24 6.89543 24 8V9C28.9744 10.6667 32 15.3333 32 20V25L34 29H6L8 25V20C8 15.3333 11.0256 10.6667 16 9V8Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        
        {/* Bell clapper */}
        <motion.path
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{ duration: 1, delay: 0.8 }}
          d="M14 29V31C14 33.2091 16.0117 35 18.5 35H21.5C23.9883 35 26 33.2091 26 31V29"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        
        {/* Notification dot */}
        <motion.circle
          initial={{ scale: 0 }}
          animate={{ scale: [0, 1.5, 1] }}
          transition={{ 
            delay: 1.5, 
            duration: 0.5, 
            ease: "easeInOut" 
          }}
          cx="29" cy="14" r="4"
          fill="hsl(var(--primary))"
        />
        
        {/* Ringing animation */}
        <motion.g
          animate={{
            rotate: [0, -5, 5, -5, 0]
          }}
          transition={{
            delay: 2,
            duration: 0.5,
            repeat: 3,
            repeatDelay: 4
          }}
        >
          <motion.path
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: [0, 0.5, 0], scale: [0.9, 1.1, 1.3] }}
            transition={{
              delay: 2,
              duration: 1,
              repeat: 3,
              repeatDelay: 4
            }}
            d="M32 20C32 12.268 25.732 6 18 6C10.268 6 4 12.268 4 20"
            stroke="hsl(var(--primary))"
            strokeWidth="1"
            strokeLinecap="round"
            strokeDasharray="2 2"
            fill="none"
          />
        </motion.g>
      </motion.svg>
    </div>
  )
}
