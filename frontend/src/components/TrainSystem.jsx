import { useState } from "react";
import axios from "axios";
import Button from "./Button";

function TrainSystem() {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleTrain = async () => {
    try {
      const response = await axios.post("http://localhost:8000/train");
      setMessage(response.data.message);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Training failed");
      setMessage("");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">
        Train RAG System
      </h2>
      <Button variant="success" onClick={handleTrain}>
        Train System
      </Button>
      {message && <p className="mt-2 text-accent">{message}</p>}
      {error && <p className="mt-2 text-red-600">{error}</p>}
    </div>
  );
}

export default TrainSystem;
