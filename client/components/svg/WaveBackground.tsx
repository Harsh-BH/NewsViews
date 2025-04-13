"use client"

export const WaveBackground = ({ className }: { className?: string }) => {
  return (
    <div className={`absolute w-full h-full overflow-hidden pointer-events-none ${className}`}>
      <svg 
        className="absolute w-full opacity-10 dark:opacity-5" 
        viewBox="0 0 1440 320" 
        xmlns="http://www.w3.org/2000/svg"
        style={{ top: '50%', transform: 'translateY(-50%)' }}
      >
        <path 
          fill="currentColor" 
          fillOpacity="1" 
          d="M0,224L40,213.3C80,203,160,181,240,160C320,139,400,117,480,122.7C560,128,640,160,720,181.3C800,203,880,213,960,202.7C1040,192,1120,160,1200,138.7C1280,117,1360,107,1400,101.3L1440,96L1440,320L1400,320C1360,320,1280,320,1200,320C1120,320,1040,320,960,320C880,320,800,320,720,320C640,320,560,320,480,320C400,320,320,320,240,320C160,320,80,320,40,320L0,320Z"
          className="wave wave1"
        >
        </path>
        <path 
          fill="currentColor" 
          fillOpacity="0.7" 
          d="M0,288L40,272C80,256,160,224,240,218.7C320,213,400,235,480,224C560,213,640,171,720,170.7C800,171,880,213,960,218.7C1040,224,1120,192,1200,170.7C1280,149,1360,139,1400,133.3L1440,128L1440,320L1400,320C1360,320,1280,320,1200,320C1120,320,1040,320,960,320C880,320,800,320,720,320C640,320,560,320,480,320C400,320,320,320,240,320C160,320,80,320,40,320L0,320Z"
          className="wave wave2"
        >
        </path>
      </svg>
      
      <style jsx>{`
        .wave {
          fill: hsl(var(--primary));
        }
        .wave1 {
          animation: moveWave1 15s linear infinite;
        }
        .wave2 {
          animation: moveWave2 20s linear infinite;
          animation-delay: -5s;
        }
        
        @keyframes moveWave1 {
          0% {
            transform: translateX(0%);
          }
          50% {
            transform: translateX(-25%);
          }
          100% {
            transform: translateX(0%);
          }
        }
        
        @keyframes moveWave2 {
          0% {
            transform: translateX(0%);
          }
          50% {
            transform: translateX(25%);
          }
          100% {
            transform: translateX(0%);
          }
        }
      `}</style>
    </div>
  )
}
