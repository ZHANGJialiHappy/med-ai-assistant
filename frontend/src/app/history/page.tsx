"use client";
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";

interface HistoryItem {
  query?: string;
  file?: string;
  result: string;
  [key: string]: any;
}

export default function History() {
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem("history");
    if (stored) {
      setHistory(JSON.parse(stored));
    }
  }, []);

  return (
    <div>
      <main className="max-w-2xl mx-auto mt-8">
        <h2 className="font-bold mb-4">History</h2>
        {history.length === 0 ? (
          <div>No history records found.</div>
        ) : (
          <ul>
            {history.map((item, idx) => (
              <li key={idx} className="mb-4 p-2 border rounded">
                <div>
                  <strong>{item.query ? "Question" : "File"}:</strong>{" "}
                  {item.query || item.file}
                </div>
                <div>
                  <strong>Result:</strong>
                  <pre className="whitespace-pre-wrap">{item.result}</pre>
                </div>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
