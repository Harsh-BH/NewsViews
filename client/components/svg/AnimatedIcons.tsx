"use client"

import { motion } from "framer-motion"

export const FilterIcon = () => {
  return (
    <motion.svg 
      width="40" 
      height="40" 
      viewBox="0 0 40 40"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <motion.path
        d="M6 8h28M10 20h20M14 32h12"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 1, delay: 0.2 }}
      />
      
      <motion.circle
        cx="26" cy="8" r="3"
        fill="hsl(var(--primary))"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 200, damping: 10, delay: 1 }}
      />
      
      <motion.circle
        cx="14" cy="20" r="3"
        fill="hsl(var(--primary))"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 200, damping: 10, delay: 1.2 }}
      />
      
      <motion.circle
        cx="20" cy="32" r="3"
        fill="hsl(var(--primary))"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 200, damping: 10, delay: 1.4 }}
      />
    </motion.svg>
  )
}

export const BookmarkIcon = () => {
  return (
    <motion.svg
      width="40"
      height="40"
      viewBox="0 0 40 40"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Bookmark outline */}
      <motion.path
        d="M10 35V8C10 6.89543 10.8954 6 12 6H28C29.1046 6 30 6.89543 30 8V35L20 29L10 35Z"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 1, delay: 0.2 }}
      />
      
      {/* Bookmark fill animation */}
      <motion.path
        d="M10 35V8C10 6.89543 10.8954 6 12 6H28C29.1046 6 30 6.89543 30 8V35L20 29L10 35Z"
        fill="hsl(var(--primary))"
        opacity="0.2"
        initial={{ opacity: 0 }}
        animate={{ opacity: [0, 0.4, 0.2] }}
        transition={{ delay: 1, duration: 2 }}
      />
      
      {/* Star in bookmark */}
      <motion.path
        d="M20 10L21.8 15.6H27.5L22.9 19.2L24.7 24.8L20 21.2L15.3 24.8L17.1 19.2L12.5 15.6H18.2L20 10Z"
        fill="hsl(var(--primary))"
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: "spring", delay: 1.2, duration: 0.5 }}
      />
    </motion.svg>
  )
}

export const ModerationIcon = () => {
  return (
    <motion.svg
      width="40"
      height="40"
      viewBox="0 0 40 40"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Shield outline */}
      <motion.path
        d="M20 34C20 34 33 28 33 20V9L20 4L7 9V20C7 28 20 34 20 34Z"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 1, delay: 0.2 }}
      />
      
      {/* Shield fill */}
      <motion.path
        d="M20 34C20 34 33 28 33 20V9L20 4L7 9V20C7 28 20 34 20 34Z"
        fill="hsl(var(--primary))"
        opacity="0.2"
        initial={{ opacity: 0 }}
        animate={{ opacity: [0, 0.3, 0.2] }}
        transition={{ delay: 1, duration: 1.5 }}
      />
      
      {/* Checkmark */}
      <motion.path
        d="M15 20.5L18 23.5L25 16.5"
        stroke="hsl(var(--primary))"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ delay: 1.3, duration: 0.7 }}
      />
    </motion.svg>
  )
}
