"use client"

export const CircuitPattern = ({ className }: { className?: string }) => {
  return (
    <div className={`absolute w-full h-full overflow-hidden pointer-events-none ${className}`}>
      <svg
        className="absolute w-full h-full opacity-[0.07] dark:opacity-[0.03]"
        viewBox="0 0 100 100"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Horizontal and vertical grid lines */}
        <g className="text-primary">
          {[...Array(10)].map((_, i) => (
            <line
              key={`h-${i}`}
              x1="0"
              y1={i * 10}
              x2="100"
              y2={i * 10}
              strokeWidth="0.2"
              stroke="currentColor"
              strokeDasharray="1 3"
            />
          ))}
          {[...Array(10)].map((_, i) => (
            <line
              key={`v-${i}`}
              x1={i * 10}
              y1="0"
              x2={i * 10}
              y2="100"
              strokeWidth="0.2"
              stroke="currentColor"
              strokeDasharray="1 3"
            />
          ))}
        </g>

        {/* Animated circuit paths */}
        <path 
          className="circuit-path path1"
          d="M10,10 L30,10 L30,30 L50,30 L50,70 L70,70 L70,90 L90,90" 
          stroke="currentColor"
          strokeWidth="0.5"
          fill="none"
        />
        
        <path 
          className="circuit-path path2"
          d="M10,50 L40,50 L40,80 L60,80 L60,20 L90,20" 
          stroke="currentColor"
          strokeWidth="0.5"
          fill="none"
        />
        
        <path 
          className="circuit-path path3"
          d="M50,10 L50,40 L80,40 L80,60 L20,60 L20,90" 
          stroke="currentColor"
          strokeWidth="0.5"
          fill="none"
        />

        {/* Animated dots */}
        <circle className="circuit-dot dot1" cx="10" cy="10" r="0.7" fill="currentColor" />
        <circle className="circuit-dot dot2" cx="50" cy="30" r="0.7" fill="currentColor" />
        <circle className="circuit-dot dot3" cx="70" cy="70" r="0.7" fill="currentColor" />
        <circle className="circuit-dot dot4" cx="40" cy="50" r="0.7" fill="currentColor" />
        <circle className="circuit-dot dot5" cx="60" cy="20" r="0.7" fill="currentColor" />
        <circle className="circuit-dot dot6" cx="50" cy="40" r="0.7" fill="currentColor" />
        <circle className="circuit-dot dot7" cx="20" cy="60" r="0.7" fill="currentColor" />
      </svg>
      
      <style jsx>{`
        .circuit-path {
          stroke-dasharray: 100;
          stroke-dashoffset: 100;
          stroke: hsl(var(--primary));
        }
        
        .path1 {
          animation: drawPath 15s infinite;
          animation-delay: 0s;
        }
        
        .path2 {
          animation: drawPath 12s infinite;
          animation-delay: 5s;
        }
        
        .path3 {
          animation: drawPath 18s infinite;
          animation-delay: 2s;
        }
        
        .circuit-dot {
          fill: hsl(var(--primary));
          opacity: 0;
        }
        
        .dot1, .dot2, .dot3 {
          animation: pulseDot 15s infinite;
        }
        
        .dot4, .dot5 {
          animation: pulseDot 12s infinite;
          animation-delay: 5s;
        }
        
        .dot6, .dot7 {
          animation: pulseDot 18s infinite;
          animation-delay: 2s;
        }
        
        @keyframes drawPath {
          0%, 10% {
            stroke-dashoffset: 100;
            opacity: 0.3;
          }
          30%, 70% {
            stroke-dashoffset: 0;
            opacity: 1;
          }
          90%, 100% {
            stroke-dashoffset: -100;
            opacity: 0.3;
          }
        }
        
        @keyframes pulseDot {
          0%, 10% {
            opacity: 0;
            r: 0.3;
          }
          30% {
            opacity: 1;
            r: 1;
          }
          50% {
            opacity: 1;
            r: 0.7;
          }
          70% {
            opacity: 1;
            r: 1;
          }
          90%, 100% {
            opacity: 0;
            r: 0.3;
          }
        }
      `}</style>
    </div>
  )
}
