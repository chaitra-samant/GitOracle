import { Link,Zap, MessageCircle,ArrowRight } from "lucide-react";
const Lworks=()=>{
    return (
      <section id="how-it-works" className="relative z-10 py-32">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              How GitOracle Works
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              How to Effortlessly Query and Analyze Your Code
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Paste Repository URL",
                description:
                  "Simply provide the GitHub repository link you want to analyze. GitOracle supports both public and private repositories.",
                icon: <Link className="w-8 h-8" />,
              },
              {
                step: "02",
                title: "AI Processes Your Code",
                description:
                  "Our advanced RAG system extracts, analyzes, and understands your entire codebase structure and functionality.",
                icon: <Zap className="w-8 h-8" />,
              },
              {
                step: "03",
                title: "Ask Anything",
                description:
                  "Query your code in natural language. Get explanations, find functions, understand dependencies, and more.",
                icon: <MessageCircle className="w-8 h-8" />,
              },
            ].map((item, index) => (
              <div key={index} className="relative group">
                <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 backdrop-blur-lg rounded-2xl border border-purple-500/20 p-8 hover:border-purple-400/40 transition-all duration-300 group-hover:scale-105">
                  <div className="text-6xl font-bold text-purple-400/20 mb-4">
                    {item.step}
                  </div>
                  <div className="bg-gradient-to-r from-purple-400 to-pink-400 p-3 rounded-xl inline-flex mb-6 group-hover:scale-110 transition-transform duration-300">
                    {item.icon}
                  </div>
                  <h3 className="text-2xl font-bold mb-4">{item.title}</h3>
                  <p className="text-gray-300 leading-relaxed">
                    {item.description}
                  </p>
                </div>
                
              </div>
            ))}
          </div>
        </div>
      </section>
    );

};
export default Lworks