import React, { useState, useEffect } from "react";
import { ArrowRight, Github } from "lucide-react";
import { useNavigate } from "react-router-dom";

const LHero = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const navigate = useNavigate();

  return (
    <section className="relative z-10 pt-20 pb-32">
      <div className="max-w-7xl mx-auto px-6">
        <div
          className={`transform transition-all duration-1000 ${
            isVisible ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          }`}
        >
          {/* Flex container for side-by-side layout */}
          <div className="flex flex-col lg:flex-row items-center justify-between gap-16">
            {/* Left: Hero content */}
            <div className="text-center lg:text-left flex-1">
              <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
                Understand Any Codebase
                <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-purple-600 bg-clip-text text-transparent block">
                  In Seconds
                </span>
              </h1>
              <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-xl leading-relaxed mx-auto lg:mx-0">
                Analyze GitHub repositories. Understand module dependencies,
                function behaviour, and design patterns in seconds
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col md:flex-row gap-4 justify-center lg:justify-start items-center mb-10">
                <button onClick={()=>navigate("/main")}
                className="group bg-gradient-to-r from-purple-500 to-pink-500 px-8 py-4 rounded-full text-lg font-semibold hover:shadow-2xl hover:shadow-purple-500/30 transition-all duration-300 transform hover:scale-105 flex items-center space-x-2">
                  <span>Try GitOracle</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
                <a
                  href="https://github.com/chaitra-samant/GitOracle"
                  target="blank"
                  className="group border-2 border-purple-400/50 px-8 py-4 rounded-full text-lg font-semibold hover:bg-purple-500/10 transition-all duration-300 flex items-center space-x-2"
                >
                  <Github className="w-5 h-5" />
                  <span>View on GitHub</span>
                </a>
              </div>
            </div>

            {/* Right: Demo Preview */}
            <div className="flex-1 w-full max-w-2xl">
              <div className="mb-6">
                <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent text-lg font-semibold">
                  🚀 Simplifying Codebases
                </span>
              </div>
              <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 backdrop-blur-lg rounded-2xl border border-purple-500/20 p-1">
                <div className="bg-slate-900/80 rounded-xl p-6 backdrop-blur-sm">
                  <div className="flex items-center space-x-2 mb-4">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  </div>
                  <div className="text-left">
                    <div className="text-gray-400 mb-2">
                      $ gitoracle analyze https://github.com/user/repo
                    </div>
                    <div className="text-purple-400 mb-4">
                      ✨ Repository analyzed successfully!
                    </div>
                    <div className="bg-gradient-to-r from-purple-500/20 to-transparent p-4 rounded-lg mb-4">
                      <div className="text-gray-300">
                        "What does the authentication function do?"
                      </div>
                    </div>
                    <div className="text-gray-200 leading-relaxed">
                      The authentication function validates user credentials
                      using JWT tokens. It checks for token expiration, verifies
                      the signature, and returns user permissions...
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          {/* End of Flex Container */}
        </div>
      </div>
    </section>
  );
};

export default LHero;
