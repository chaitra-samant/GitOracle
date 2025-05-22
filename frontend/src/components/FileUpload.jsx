import { useState } from "react";
import axios from "axios";
import Button from "./Button";

function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setMessage(response.data.message);
      setError("");
      setFile(null);
      if (onUploadSuccess) onUploadSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
      setMessage("");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">
        Upload Document
      </h2>
      <input
        type="file"
        accept=".txt,.pdf,.docx"
        onChange={handleFileChange}
        className="mb-4 w-full text-gray-700"
      />
      <Button onClick={handleUpload} disabled={!file}>
        Upload
      </Button>
      {message && <p className="mt-2 text-accent">{message}</p>}
      {error && <p className="mt-2 text-red-600">{error}</p>}
    </div>
  );
}

export default FileUpload;
