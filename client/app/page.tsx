"use client"

// Remove unused import
// import { EnhancedDataVisual } from "@/components/svg/EnhancedDataVisual"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ModeToggle } from "@/components/mode-toggle"
import { motion, useScroll, useTransform } from "framer-motion"
import { ArrowRight, Globe, MessageSquare, Shield } from "lucide-react"
// Remove unused imports: BookmarkIcon, Filter, Star
import dynamic from 'next/dynamic'
import Link from "next/link"
import { useRef } from "react"

// Import SVG components
import { 
  MessageSvg, 
  NewsSvg, 
  NetworkSvg, 
  BubblesSvg,
  NewsIconsSvg
} from "@/components/svg/AnimatedSvgCollection"

import { FilterIcon, BookmarkIcon as AnimatedBookmark, ModerationIcon } from "@/components/svg/AnimatedIcons"

// Dynamically import the AnimatedStars component
const AnimatedStars = dynamic(() => import('@/components/AnimatedStars'), { 
  ssr: false 
})

export default function Home() {
  // Parallax scroll references
  const containerRef = useRef(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  })
  
  // Fix: Remove the ease option from all useTransform calls
  const heroY = useTransform(scrollYProgress, [0, 0.5], [0, -100])
  const heroScale = useTransform(scrollYProgress, [0, 0.2], [1, 0.95])
  const featuresY = useTransform(scrollYProgress, [0.2, 0.6], [100, -50])
  const ctaScale = useTransform(scrollYProgress, [0.6, 0.8], [0.9, 1])
  const starsOpacity = useTransform(scrollYProgress, [0, 0.4], [1, 0])
  
  // Additional parallax effects without ease options
  const networkX = useTransform(scrollYProgress, [0.1, 0.5], [-20, 20])
  const bubblesY = useTransform(scrollYProgress, [0.3, 0.7], [50, -50])
  const messageX = useTransform(scrollYProgress, [0.1, 0.3], [50, -20])
  
  // New parallax effects without ease options
  const heroElementsY = useTransform(scrollYProgress, [0, 0.3], [0, -50])
  const featureCardsX = useTransform(scrollYProgress, [0.4, 0.6], [-10, 10])
  const featureCardsStagger = [
    useTransform(scrollYProgress, [0.4, 0.6], [0, -15]),
    useTransform(scrollYProgress, [0.4, 0.6], [0, 0]),
    useTransform(scrollYProgress, [0.4, 0.6], [0, 15]),
  ]
  
  return (
    <div ref={containerRef} className="min-h-screen bg-gradient-to-b from-background to-muted dark:from-background dark:to-background/80 relative overflow-hidden">
      {/* Animated backgrounds */}
      <AnimatedStars starsOpacity={starsOpacity} />
      
      {/* Floating network animations in the background */}
      <motion.div 
        className="absolute inset-0 opacity-30 dark:opacity-10"
        style={{ x: networkX }}
      >
        <NetworkSvg />
      </motion.div>
      
      {/* Floating bubbles with parallax */}
      <motion.div 
        className="absolute right-0 top-0 w-full h-full opacity-20 dark:opacity-10 pointer-events-none"
        style={{ y: bubblesY }}
      >
        <BubblesSvg />
      </motion.div>
      
      {/* Navigation with theme toggle */}
      <nav className="container mx-auto px-4 py-6 flex justify-between items-center sticky top-0 z-50 backdrop-blur-sm bg-background/80 dark:bg-background/80 border-b border-border/40">
        <motion.div 
          className="flex items-center"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h3 className="text-xl font-bold"><span className="text-primary">News</span>Views</h3>
        </motion.div>
        <div className="flex items-center space-x-6">
          <motion.div 
            className="hidden md:flex space-x-6 items-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Link href="#" className="hover:text-primary transition-colors">Features</Link>
            <Link href="#" className="hover:text-primary transition-colors">How It Works</Link>
            <Link href="#" className="hover:text-primary transition-colors">About</Link>
          </motion.div>
          <ModeToggle />
        </div>
      </nav>

      {/* Hero Section with enhanced parallax */}
      <section className="container mx-auto px-4 py-24 md:py-32 relative">
        {/* Floating elements with depth */}
        <motion.div 
          className="absolute w-20 h-20 top-12 right-[10%] opacity-20 dark:opacity-10 hidden md:block"
          style={{ y: heroElementsY, rotate: useTransform(scrollYProgress, [0, 0.3], [0, 10]) }}
        >
          <svg viewBox="0 0 100 100" className="w-full h-full">
            <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" strokeWidth="1" strokeDasharray="5 5" />
          </svg>
        </motion.div>
        
        <motion.div 
          className="absolute w-16 h-16 bottom-12 left-[12%] opacity-20 dark:opacity-10 hidden md:block"
          style={{ y: useTransform(scrollYProgress, [0, 0.3], [0, -30]), rotate: useTransform(scrollYProgress, [0, 0.3], [0, -10]) }}
        >
          <svg viewBox="0 0 100 100" className="w-full h-full">
            <rect x="20" y="20" width="60" height="60" fill="none" stroke="currentColor" strokeWidth="1" />
          </svg>
        </motion.div>
        
        <div className="flex flex-col md:flex-row items-center justify-between">
          <motion.div 
            className="text-center md:text-left space-y-6 md:w-1/2"
            style={{ y: heroY, scale: heroScale }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ 
                duration: 1,
                type: "spring",
                stiffness: 100
              }}
            >
              <motion.h1 
                className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight"
                animate={{ 
                  backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"]
                }}
                transition={{
                  duration: 10,
                  repeat: Infinity,
                  ease: "linear"
                }}
                style={{
                  backgroundImage: "linear-gradient(90deg, hsl(var(--primary)) 0%, hsl(var(--secondary)) 50%, hsl(var(--primary)) 100%)",
                  backgroundSize: "200% auto",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                }}
              >
                NewsViews
              </motion.h1>
            </motion.div>
            <motion.p 
              className="text-xl text-muted-foreground max-w-2xl mx-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.8 }}
            >
              Community-driven news aggregator that brings local news to your fingertips
            </motion.p>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="flex flex-col sm:flex-row justify-center md:justify-start gap-4"
            >
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                <Button size="lg" className="relative overflow-hidden group">
                  <span className="relative z-10">Browse News</span>
                  <ArrowRight className="ml-2 h-4 w-4 relative z-10 transition-transform group-hover:translate-x-1" />
                  <motion.span 
                    className="absolute inset-0 bg-primary-foreground dark:bg-primary-foreground mix-blend-soft-light"
                    initial={{ x: "-100%" }}
                    whileHover={{ x: "0%" }}
                    transition={{ duration: 0.3 }}
                  />
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                <Button size="lg" variant="outline" className="border-primary/20 hover:border-primary">
                  Submit News
                </Button>
              </motion.div>
            </motion.div>
          </motion.div>
          
          <motion.div 
            className="mt-10 md:mt-0 md:w-1/2 flex justify-center relative"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4, duration: 1 }}
          >
            {/* Main hero animation */}
            <div className="w-full max-w-md relative z-10">
              <NewsSvg />
            </div>
            
            {/* Message animation with parallax */}
            <motion.div 
              className="absolute w-32 h-32 top-[10%] -left-[5%] z-20"
              style={{ x: messageX }}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8, duration: 0.5 }}
            >
              <MessageSvg />
            </motion.div>
            
            {/* Floating news icons */}
            <motion.div 
              className="absolute w-24 h-24 bottom-[5%] right-[5%] z-20"
              animate={{ 
                y: [0, -10, 0],
                rotate: [0, 5, 0]
              }}
              transition={{ 
                duration: 5, 
                repeat: Infinity,
                ease: "easeInOut" 
              }}
            >
              <NewsIconsSvg />
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-4 py-16 md:py-24 relative">
        <motion.div 
          className="absolute top-24 -left-36 w-72 h-72 bg-primary/5 dark:bg-primary/10 rounded-full blur-3xl"
          animate={{ 
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ 
            duration: 8, 
            repeat: Infinity,
            ease: "easeInOut" 
          }}
        />
        
        <motion.div 
          className="text-center mb-16 relative z-10"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">How It Works</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">Our streamlined process brings community news to everyone</p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              title: "Submit",
              description: "Community members submit local news through a simple Google Form",
              icon: <MessageSquare className="h-10 w-10 text-primary" />
            },
            {
              title: "Process",
              description: "Our system validates, filters, and moderates all submissions",
              icon: <Shield className="h-10 w-10 text-primary" />
            },
            {
              title: "Browse",
              description: "Browse concise, Inshorts-style news cards in a beautiful feed",
              icon: <Globe className="h-10 w-10 text-primary" />
            }
          ].map((item, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2, duration: 0.8 }}
              whileHover={{ y: -10 }}
            >
              <Card className="h-full transition-all hover:shadow-lg dark:border-muted/20 dark:bg-muted/10 dark:backdrop-blur">
                <CardHeader className="text-center">
                  <motion.div 
                    className="mx-auto mb-4 p-4 rounded-full bg-primary/10 dark:bg-primary/20"
                    initial={{ rotate: 0 }}
                    whileHover={{ rotate: 5, scale: 1.1 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    {item.icon}
                  </motion.div>
                  <CardTitle>{item.title}</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <p>{item.description}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
        
        {/* Enhanced data visualization with parallax */}
    
      </section>

      {/* Features Section with enhanced parallax */}
      <section className="container mx-auto px-4 py-16 md:py-24 relative overflow-hidden">
        <motion.div 
          className="absolute top-0 -right-36 w-96 h-96 bg-secondary/10 dark:bg-secondary/5 rounded-full blur-3xl"
          animate={{ 
            x: [0, 20, 0],
            y: [0, -30, 0],
          }}
          transition={{ 
            duration: 10, 
            repeat: Infinity,
            ease: "easeInOut" 
          }}
        />

        <motion.div 
          className="text-center mb-16 relative z-10"
          style={{ y: featuresY }}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Key Features</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">Designed to deliver the best community news experience</p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              title: "Smart Filtering",
              description: "Intelligent filters ensure quality and relevance of all news items",
              icon: <FilterIcon />
            },
            {
              title: "Bookmarking",
              description: "Save your favorite news stories to read later",
              icon: <AnimatedBookmark />
            },
            {
              title: "Community Moderation",
              description: "Trusted community members help ensure content quality",
              icon: <ModerationIcon />
            }
          ].map((feature, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, scale: 0.95, y: 30 }}
              whileInView={{ opacity: 1, scale: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ 
                delay: index * 0.1, 
                duration: 0.6,
                type: "spring",
                stiffness: 50,
                damping: 15 
              }}
              whileHover={{ 
                y: -12, 
                transition: { 
                  type: "spring",
                  stiffness: 300,
                  damping: 15,
                  duration: 0.2 
                } 
              }}
              className="flex flex-col"
              style={{ x: featureCardsX, y: featureCardsStagger[index] }}
            >
              <Card className="h-full border-none shadow-md bg-gradient-to-br from-background to-muted dark:from-muted/10 dark:to-background">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    {feature.icon}
                  </div>
                  <CardTitle className="flex items-center justify-center">
                    {feature.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-center">{feature.description}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA Section with enhanced gradient and parallax */}
      <section className="container mx-auto px-4 py-24 relative">
        <motion.div 
          className="max-w-4xl mx-auto text-center rounded-2xl overflow-hidden relative"
          style={{ scale: ctaScale }}
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 1 }}
        >
          {/* Background gradient animation */}
          <motion.div 
            className="absolute inset-0 bg-gradient-to-r from-primary/30 to-secondary/20 dark:from-primary/20 dark:to-secondary/10"
            animate={{ 
              backgroundPosition: ["0% 0%", "100% 100%", "0% 0%"]
            }}
            transition={{ 
              duration: 15, 
              repeat: Infinity,
              ease: "linear" 
            }}
          />
          
          {/* Background network pattern */}
          <div className="absolute inset-0 opacity-10">
            <NetworkSvg delay={2} />
          </div>
          
          {/* Content */}
          <div className="relative z-10 p-10">
            <motion.h2 
              className="text-3xl font-bold mb-4"
              animate={{ 
                textShadow: ["0 0 0px rgba(0,0,0,0)", "0 0 10px rgba(var(--primary-rgb), 0.3)", "0 0 0px rgba(0,0,0,0)"]
              }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              Ready to join our community?
            </motion.h2>
            <p className="text-lg text-muted-foreground mb-8">Start browsing local news or contribute by submitting your own stories</p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                <Link href="/news" className="relative overflow-hidden group">
                <Button size="lg" className="relative overflow-hidden group ">
                  <span className="relative z-10">Browse News Feed</span>
                  <motion.div 
                    className="absolute inset-0 bg-primary-foreground mix-blend-soft-light"
                    initial={{ scale: 0, borderRadius: "100%" }}
                    whileHover={{ scale: 1.5, borderRadius: "0%" }}
                    transition={{ duration: 0.4 }}
                  />
                </Button>
                </Link>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
                <Button size="lg" variant="outline" className="border-primary/20 hover:border-primary">
                  Submit a Story
                </Button>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-10 border-t dark:border-muted/20">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h3 className="text-xl font-bold"><span className="text-primary">News</span>Views</h3>
            <p className="text-muted-foreground">FY25Q2 Internship Assignment Project</p>
          </div>
          <div className="flex gap-6">
            <Link href="#" className="text-muted-foreground hover:text-primary transition-colors">About</Link>
            <Link href="#" className="text-muted-foreground hover:text-primary transition-colors">Privacy</Link>
            <Link href="#" className="text-muted-foreground hover:text-primary transition-colors">Contact</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
