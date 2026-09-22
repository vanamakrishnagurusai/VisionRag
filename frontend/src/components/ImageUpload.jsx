import { useState } from "react";
import { API_BASE_URL } from "../config";

function ImageUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setMessage("");
    setError("");

    if (!selectedFile) {
      setFile(null);
      return;
    }

    const allowedTypes = [
      "image/jpeg",
      "image/jpg",
      "image/png",
      "image/webp",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setError("Please select a JPG, PNG or WEBP image.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an image first.");
      return;
    }

    setUploading(true);
    setMessage("");
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${API_BASE_URL}/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Upload failed."
        );
      }

      setMessage(
        `Uploaded and indexed: ${data.image.filename}`
      );

      setFile(null);

      if (onUploadSuccess) {
        onUploadSuccess(data.image);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mb-8 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

      <h2 className="mb-2 text-xl font-semibold text-gray-900">
        Upload Image
      </h2>

      <p className="mb-4 text-sm text-gray-500">
        Upload a new image to add it to the VisionRAG search index.
      </p>

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">

        <input
          type="file"
          accept=".jpg,.jpeg,.png,.webp"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-600"
        />

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="rounded-lg bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload Image"}
        </button>

      </div>

      {file && (
        <p className="mt-3 text-sm text-gray-600">
          Selected: {file.name}
        </p>
      )}

      {message && (
        <p className="mt-4 rounded-lg bg-green-50 p-3 text-sm text-green-700">
          ✓ {message}
        </p>
      )}

      {error && (
        <p className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      )}

    </div>
  );
}

export default ImageUpload;