import { useState, useEffect } from "react";
import axios from "axios";
import Button from "./Button";

function StatusDisplay() {
  const [status, setStatus] = useState("");
  const [message, setMessage] = useState("");

  const checkStatus = async () => {
    try {
      const response = await axios.get("http://localhost:8000/status");
      setStatus(response.data.status);
      setMessage(response.data.message);
    } catch (err) {
      setStatus("error");
      setMessage("Failed to check status");
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">
        System Status
      </h2>
      <p
        className={`mb-4 ${
          status === "ready" ? "text-accent" : "text-red-600"
        }`}
      >
        Status: {message}
      </p>
      <Button onClick={checkStatus}>Refresh Status</Button>
    </div>
  );
}

export default StatusDisplay;
