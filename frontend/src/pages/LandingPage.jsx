import { Link } from "react-router-dom";
import Button from "../components/Button";

function LandingPage() {
  return (
    <div className="min-h-screen bg-neutral flex flex-col justify-center items-center text-center px-4">
      <h1 className="text-4xl md:text-5xl font-bold text-primary mb-6">
        Welcome to the RAG System
      </h1>
      <p className="text-lg md:text-xl text-gray-700 mb-8 max-w-2xl">
        Upload documents, train the system, and query information with ease. Our
        Retrieval-Augmented Generation system is designed to provide accurate
        and context-aware responses.
      </p>
      <Link to="/app">
        <Button variant="primary">Get Started</Button>
      </Link>
    </div>
  );
}

export default LandingPage;
