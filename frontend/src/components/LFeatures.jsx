import React, { useState, useEffect } from "react";
import { Github, Search, Zap } from "lucide-react";

const LFeatures = () => {
  const [activeFeature, setActiveFeature] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % 3);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: <Github className="w-8 h-8" />,
      title: "Repository Analysis",
      description:
        "Simply paste any GitHub repository URL and GitOracle extracts your entire codebase and structure.",
      color: "from-purple-400 to-pink-400",
    },
    {
      icon: <Search className="w-8 h-8" />,
      title: "Natural Language Queries",
      description:
        "Ask questions about functions, files, and code logic in plain English. No more digging through documentation.",
      color: "from-purple-400 to-pink-400",
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Instant Understanding",
      description:
        "Get intelligent responses about code functionality, dependencies, and architecture in seconds.",
      color: "from-purple-400 to-pink-400",
    },
  ];

  return (
    <section id="features" className="relative z-10 py-32">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-20">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Powerful Features for
            <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              {" "}
              Software Development
            </span>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            GitOracle combines advanced AI with deep code understanding to
            revolutionize how you interact with repositories.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className={`group relative bg-gradient-to-br ${
                feature.color
              } p-0.5 rounded-2xl hover:shadow-2xl transition-all duration-500 hover:scale-105 ${
                activeFeature === index ? "scale-105 shadow-2xl" : ""
              }`}
            >
              <div className="bg-slate-900/90 backdrop-blur-lg rounded-2xl p-8 h-full">
                <div
                  className={`inline-flex p-4 rounded-xl bg-gradient-to-r ${feature.color} mb-6 group-hover:scale-110 transition-transform duration-300`}
                >
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-4 text-white">
                  {feature.title}
                </h3>
                <p className="text-gray-300 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default LFeatures;
