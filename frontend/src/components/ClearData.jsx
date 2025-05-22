import { useState } from "react";
import axios from "axios";
import Button from "./Button";

function ClearData({ onClearSuccess }) {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleClear = async () => {
    try {
      const response = await axios.post("http://localhost:8000/clear");
      setMessage(response.data.message);
      setError("");
      if (onClearSuccess) onClearSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to clear data");
      setMessage("");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Clear Data</h2>
      <Button variant="danger" onClick={handleClear}>
        Clear All Data
      </Button>
      {message && <p className="mt-2 text-accent">{message}</p>}
      {error && <p className="mt-2 text-red-600">{error}</p>}
    </div>
  );
}

export default ClearData;
