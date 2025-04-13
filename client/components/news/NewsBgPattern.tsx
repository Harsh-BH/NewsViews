export default function NewsBgPattern() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      <svg
        className="absolute right-0 top-0 h-full w-1/2 translate-x-1/2 opacity-10"
        fill="none"
        viewBox="0 0 400 400"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g>
          <path
            d="M289.8 20.7c27.3 18 42.5 52.1 43.7 86.6 1.3 34.4-11.3 69.3-39.3 87.6-28 18.3-71.5 20-105.5 2.3-34-17.7-58.3-54.8-47.8-87s56-60.4 99.3-73.4c43.4-13.1 86.4-6.8 102.7 4.3 16.3 11.2 16.3 35.2 16.3 59.2s0 48.1-11.2 62.6c-11.1 14.5-33.3 17.6-43.7 8.6"
            stroke="#2563EB"
            strokeLinecap="round"
            strokeWidth="2"
            opacity="0.8"
          ></path>
        </g>
      </svg>
      <svg
        className="absolute left-0 bottom-0 h-full w-1/2 -translate-x-1/2 opacity-10"
        fill="none"
        viewBox="0 0 400 400"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g>
          <path
            d="M289.8 20.7c27.3 18 42.5 52.1 43.7 86.6 1.3 34.4-11.3 69.3-39.3 87.6-28 18.3-71.5 20-105.5 2.3-34-17.7-58.3-54.8-47.8-87s56-60.4 99.3-73.4c43.4-13.1 86.4-6.8 102.7 4.3 16.3 11.2 16.3 35.2 16.3 59.2s0 48.1-11.2 62.6c-11.1 14.5-33.3 17.6-43.7 8.6"
            stroke="#2563EB"
            strokeLinecap="round"
            strokeWidth="2"
            opacity="0.8"
          ></path>
        </g>
      </svg>
      <div className="absolute top-0 w-full h-20 bg-gradient-to-b from-blue-50 to-transparent"></div>
      <div className="absolute bottom-0 w-full h-20 bg-gradient-to-t from-blue-50 to-transparent"></div>
    </div>
  );
}
