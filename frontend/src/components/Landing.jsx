import LHeader from "./LHeader";
import LHero from "./LHero";
import LFeatures from "./LFeatures";
import Lworks from "./LWorks";
import LFooter from "./LFooter";

const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden m-0 p-0">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div
          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-purple-500/5 to-pink-500/5 rounded-full blur-3xl animate-spin"
          style={{ animationDuration: "20s" }}
        ></div>
      </div>

      <LHeader/>
      <LHero/>
      <LFeatures/>
      <Lworks/>
      <LFooter/>
      
    </div>
  );
};

export default Landing;
