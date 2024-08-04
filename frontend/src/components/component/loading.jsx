import React from 'react';


const LoadingAnimation = () => {
  return (
    <>
      <style>{styles}</style>
      <div className="flex flex-col gap-12 justify-center items-center h-screen">
        <p>Cooking up your game...</p>
        <WaffleIcon className="animate-loading z-10"/>
        <OvalShadow className="relative bottom-24 opacity-75 w-32"/>
      </div>
    </>
  );
};

const styles = `
@keyframes loading {
  0% {
    transform: translateY(0) rotate(0deg);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  20% {
    transform: translateY(-30px) rotate(0deg);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
  80% {
    transform: translateY(-30px) rotate(360deg);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  100% {
    transform: translateY(0)  rotate(360deg);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

.animate-loading {
  animation: loading 5s infinite;
}
`;

export default LoadingAnimation;


function WaffleIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="100"
      height="100"
      viewBox="0 0 240 240"
    >
      <defs>
        <linearGradient id="waffleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{stopColor: "#F6CA7D", stopOpacity: 1}} />
          <stop offset="100%" style={{stopColor: "#E5B667", stopOpacity: 1}} />
        </linearGradient>
        </defs>
        <g transform="translate(11, 11)">
              <rect width="218" height="218" rx="25" ry="25" fill="#8B4513"/>
        </g>
        <g transform="translate(15, 15)">
            <rect width="210" height="210" rx="20" ry="20" fill="url(#waffleGradient)"/>
        </g>
        <g fill="#D58A2F" transform="translate(15, 15)">
          <rect x="10" y="10" width="40" height="40"/>
          <rect x="60" y="10" width="40" height="40"/>
          <rect x="110" y="10" width="40" height="40"/>
          <rect x="160" y="10" width="40" height="40"/>

          <rect x="10" y="60" width="40" height="40"/>
          <rect x="60" y="60" width="40" height="40"/>
          <rect x="110" y="60" width="40" height="40"/>
          <rect x="160" y="60" width="40" height="40"/>

          <rect x="10" y="110" width="40" height="40"/>
          <rect x="60" y="110" width="40" height="40"/>
          <rect x="110" y="110" width="40" height="40"/>
          <rect x="160" y="110" width="40" height="40"/>

          <rect x="10" y="160" width="40" height="40"/>
          <rect x="60" y="160" width="40" height="40"/>
          <rect x="110" y="160" width="40" height="40"/>
          <rect x="160" y="160" width="40" height="40"/>
        </g>

        <g fill="#F49F2A" transform="translate(15, 15)">
          <path d="M30 20 h20 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M75 20 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M125 20 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M175 20 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>

          <path d="M25 70 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M75 70 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M125 70 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M175 70 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>

          <path d="M25 120 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M75 120 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M125 120 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M175 120 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>

          <path d="M25 170 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M75 170 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M125 170 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
          <path d="M175 170 h25 v30 h-35 v-20 q0 -10 10 -10 z"/>
        </g>
    </svg>
  )
}


function OvalShadow(props) {
  return (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" {...props}>
    <defs>
      <radialGradient id="shadowGradient" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
        <stop offset="0%" style={{stopColor: 'rgba(0,0,0,0.5)', stopOpacity: 1}} />
        <stop offset="100%" style={{stopColor: 'rgba(0,0,0,0)', stopOpacity: 1}} />
      </radialGradient>
    </defs>
    <ellipse cx={100} cy={50} rx={80} ry={40} fill="url(#shadowGradient)" />
  </svg>
  )
};