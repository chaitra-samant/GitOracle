import { Code } from "lucide-react";
import logo2 from "../assets/logo2.jpg";

const LFooter = () => {
  return (
    <footer
      id="contact"
      className="relative z-10 border-t border-purple-500/20 py-6"
    >
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-row justify-between items-center">
          <div className="flex items-center space-x-3">
            <img
              src={logo2}
              alt="Logo"
              className="w-8 h-8 rounded-full object-cover"
            />

            <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              GitOracle
            </span>
          </div>

          <p className="text-gray-400 text-sm whitespace-nowrap">
            &copy; 2025 GitOracle. Built with ❤️ for developers.
          </p>

          <div className="flex space-x-6 text-gray-400">
            <a href="#" className="hover:text-purple-400 transition-colors">
              Privacy
            </a>
            <a href="#" className="hover:text-purple-400 transition-colors">
              Terms
            </a>
            <a href="#" className="hover:text-purple-400 transition-colors">
              Support
            </a>
            <a href="#" className="hover:text-purple-400 transition-colors">
              Docs
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default LFooter;
