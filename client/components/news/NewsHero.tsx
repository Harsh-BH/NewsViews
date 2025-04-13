'use client';

import { useEffect, useState } from 'react';

export default function NewsHero() {
  // Use state to hold random values, but only generate them client-side
  const [circles, setCircles] = useState<Array<{
    width: number;
    height: number;
    left: string;
    top: string;
    duration: string;
    delay: string;
  }>>([]);

  // Generate random values only on client-side
  useEffect(() => {
    const newCircles = Array(10).fill(0).map(() => ({
      width: Math.random() * 200 + 50,
      height: Math.random() * 200 + 50,
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      duration: `${Math.random() * 5 + 5}s`,
      delay: `${Math.random() * 2}s`,
    }));
    setCircles(newCircles);
  }, []);

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-blue-600 to-blue-800 py-16">
      {/* Animated Pattern - Only rendered client-side */}
      <div className="absolute inset-0 opacity-20">
        {circles.map((circle, i) => (
          <div
            key={i}
            className="absolute bg-white rounded-full animate-pulse"
            style={{
              width: circle.width,
              height: circle.height,
              left: circle.left,
              top: circle.top,
              animationDuration: circle.duration,
              animationDelay: circle.delay,
            }}
          />
        ))}
      </div>
      
      <div className="max-w-7xl mx-auto px-4 relative z-10">
        <div className="flex flex-col md:flex-row md:justify-between md:items-center">
          <div className="mb-8 md:mb-0 md:max-w-xl animate-fade-in">
            <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white mb-4 leading-tight">
              Stay Informed with <br />
              <span className="text-yellow-300">NewsViews</span>
            </h1>
            <p className="text-blue-100 text-lg mb-6 leading-relaxed">
              Your trusted source for local and global news, curated and fact-checked by our community of reporters.
            </p>
            
            <div className="flex items-center">
              <div className="flex -space-x-2">
                {['A', 'B', 'R', 'S'].map((letter, i) => (
                  <div
                    key={i}
                    className="w-10 h-10 rounded-full border-2 border-white bg-blue-400 flex items-center justify-center text-white text-sm font-medium animate-fade-in"
                    style={{ animationDelay: `${0.3 + i * 0.1}s` }}
                  >
                    {letter}
                  </div>
                ))}
              </div>
              <div
                className="ml-4 text-blue-100 text-sm animate-fade-in"
                style={{ animationDelay: '0.7s' }}
              >
                Trusted by <span className="font-bold text-white">10,000+</span> readers
              </div>
            </div>
          </div>
          
          <div
            className="relative animate-fade-in"
            style={{ animationDelay: '0.3s' }}
          >
            <svg className="w-full h-auto max-w-xs" viewBox="0 0 200 180" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect 
                x="25" y="25" width="150" height="130" rx="10" 
                fill="white" 
                className="animate-draw"
              />
              <rect 
                x="40" y="45" width="120" height="10" rx="2" 
                fill="#E5E7EB" 
                className="animate-grow-x"
                style={{ animationDelay: '0.7s' }}
              />
              <rect 
                x="40" y="65" width="120" height="10" rx="2" 
                fill="#E5E7EB"
                className="animate-grow-x"
                style={{ animationDelay: '0.8s' }}
              />
              <rect 
                x="40" y="85" width="80" height="10" rx="2" 
                fill="#E5E7EB"
                className="animate-grow-x"
                style={{ animationDelay: '0.9s' }}
              />
              <circle 
                cx="40" cy="120" r="10" 
                fill="#BFDBFE"
                className="animate-scale-in"
                style={{ animationDelay: '1s' }}
              />
              <circle 
                cx="75" cy="120" r="10"  
                fill="#93C5FD"
                className="animate-scale-in"
                style={{ animationDelay: '1.1s' }}
              />
              <circle 
                cx="110" cy="120" r="10"  
                fill="#60A5FA"
                className="animate-scale-in"
                style={{ animationDelay: '1.2s' }}
              />
              <circle 
                cx="145" cy="120" r="10"  
                fill="#3B82F6"
                className="animate-scale-in"
                style={{ animationDelay: '1.3s' }}
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
