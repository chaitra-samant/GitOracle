import { useState } from "react";
import axios from "axios";
import Button from "./Button";

function QueryForm() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");

  const handleQuery = async () => {
    if (!query.trim()) {
      setError("Please enter a query");
      return;
    }

    try {
      const res = await axios.post("http://localhost:8000/query", { query });
      setResponse(JSON.stringify(res.data, null, 2));
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Query failed");
      setResponse("");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">
        Query RAG System
      </h2>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query..."
        className="w-full p-2 border rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-secondary"
      />
      <Button onClick={handleQuery}>Submit Query</Button>
      {response && (
        <pre className="mt-4 p-4 bg-neutral rounded-md text-gray-800">
          {response}
        </pre>
      )}
      {error && <p className="mt-2 text-red-600">{error}</p>}
    </div>
  );
}

export default QueryForm;
