"use client";
import { useState } from "react";
import Navbar from "@/components/Navbar";

export default function Analyze() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string>("");

  const handleSubmit = async () => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    if (!file) {
      alert("Please select a PDF file.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    formData.append("age", user.age || 0);
    formData.append("gender", user.gender || "");

    const res = await fetch("http://127.0.0.1:8000/analyze_report", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setResult(data.result);
    // Save to history
    const history = JSON.parse(localStorage.getItem("history") || "[]");
    localStorage.setItem(
      "history",
      JSON.stringify([...history, { file: file.name, result: data.result }])
    );
  };

  return (
    <div>
      <main className="max-w-2xl mx-auto mt-8">
        <h2 className="font-bold mb-4">Analyze Medical Report</h2>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="mb-2"
        />
        <button
          onClick={handleSubmit}
          className="bg-blue-600 text-white px-4 py-2 rounded ml-2"
        >
          Submit
        </button>
        {result && (
          <div className="mt-4 bg-gray-100 p-4 rounded flex flex-col items-center max-w-full">
            <h3 className="font-bold mb-2">Result</h3>
            <pre className="text-center w-full whitespace-pre-wrap break-words">
              {result}
            </pre>
          </div>
        )}
      </main>
    </div>
  );
}
