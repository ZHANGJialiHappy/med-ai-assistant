"use client";
import { useState } from "react";

export default function Ask() {
  const [question, setQuestion] = useState("");
  const [indicators, setIndicators] = useState<
    { key: string; value: string }[]
  >([]);
  const [result, setResult] = useState("");
  const [indicatorKey, setIndicatorKey] = useState("");
  const [indicatorValue, setIndicatorValue] = useState("");

  const addIndicator = () => {
    if (indicatorKey && indicatorValue) {
      setIndicators([
        ...indicators,
        { key: indicatorKey, value: indicatorValue },
      ]);
      setIndicatorKey("");
      setIndicatorValue("");
    }
  };

  const handleSubmit = async () => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const indicatorsObj = Object.fromEntries(
      indicators.map((i) => [i.key, i.value])
    );
    const body = {
      query: question,
      age: user.age || 0,
      gender: user.gender || "",
      indicators: indicatorsObj,
      top_k: 3,
    };
    const res = await fetch("http://127.0.0.1:8000/rag_query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    setResult(data.result);
    const history = JSON.parse(localStorage.getItem("history") || "[]");
    localStorage.setItem(
      "history",
      JSON.stringify([...history, { ...body, result: data.result }])
    );
  };

  return (
    <div>
      <main className="max-w-2xl mx-auto mt-8">
        <h2 className="font-bold mb-4">Question</h2>
        <input
          type="text"
          placeholder="please enter your question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="border px-2 py-1 rounded w-full mb-2"
        />
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            placeholder="Indicator"
            value={indicatorKey}
            onChange={(e) => setIndicatorKey(e.target.value)}
            className="border px-2 py-1 rounded"
          />
          <input
            type="text"
            placeholder="Indicator Value"
            value={indicatorValue}
            onChange={(e) => setIndicatorValue(e.target.value)}
            className="border px-2 py-1 rounded"
          />
          <button onClick={addIndicator} className="bg-gray-200 px-2 rounded">
            add
          </button>
        </div>
        <table className="mb-4 w-full">
          <thead>
            <tr>
              <th className="text-left px-2 py-1">Indicator</th>
              <th className="text-left px-2 py-1">Indicator value</th>
            </tr>
          </thead>
          <tbody>
            {indicators.map((i, idx) => (
              <tr key={idx}>
                <td>{i.key}</td>
                <td>{i.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button
          onClick={handleSubmit}
          className="bg-blue-600 text-white px-4 py-2 rounded"
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
