"use client"

import * as React from "react"
import { MoonIcon, SunIcon, LaptopIcon } from "lucide-react"
import { useTheme } from "next-themes"
import { motion } from "framer-motion"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function ModeToggle() {
  const { setTheme, theme } = useTheme()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon" className="relative h-9 w-9 border-muted-foreground/20">
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ 
              scale: theme === "light" ? 1 : 0, 
              opacity: theme === "light" ? 1 : 0 
            }}
            className="absolute"
          >
            <SunIcon className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all" />
          </motion.div>
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ 
              scale: theme === "dark" ? 1 : 0, 
              opacity: theme === "dark" ? 1 : 0 
            }}
            className="absolute"
          >
            <MoonIcon className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all" />
          </motion.div>
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ 
              scale: theme === "system" ? 1 : 0, 
              opacity: theme === "system" ? 1 : 0 
            }}
            className="absolute"
          >
            <LaptopIcon className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all" />
          </motion.div>
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem 
          className="flex items-center gap-2 cursor-pointer"
          onClick={() => setTheme("light")}
        >
          <SunIcon className="h-4 w-4" />
          <span>Light</span>
          {theme === "light" && (
            <motion.div 
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              className="ml-auto h-1.5 w-1.5 rounded-full bg-primary"
            ></motion.div>
          )}
        </DropdownMenuItem>
        <DropdownMenuItem 
          className="flex items-center gap-2 cursor-pointer"
          onClick={() => setTheme("dark")}
        >
          <MoonIcon className="h-4 w-4" />
          <span>Dark</span>
          {theme === "dark" && (
            <motion.div 
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              className="ml-auto h-1.5 w-1.5 rounded-full bg-primary"
            ></motion.div>
          )}
        </DropdownMenuItem>
        <DropdownMenuItem 
          className="flex items-center gap-2 cursor-pointer"
          onClick={() => setTheme("system")}
        >
          <LaptopIcon className="h-4 w-4" />
          <span>System</span>
          {theme === "system" && (
            <motion.div 
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              className="ml-auto h-1.5 w-1.5 rounded-full bg-primary"
            ></motion.div>
          )}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
