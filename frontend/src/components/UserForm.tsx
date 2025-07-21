"use client";
import { useState } from "react";

export default function UserForm() {
  const [age, setAge] = useState<number | string>("");
  const [gender, setGender] = useState<string>("");
  const handleSave = () => {
    const user = { age, gender };
    localStorage.setItem("user", JSON.stringify(user));
    alert("User info saved!");
  };
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="mb-4 font-bold">User information</h2>
      <div className="flex gap-4 mb-4">
        <input
          type="number"
          placeholder="age"
          value={age}
          onChange={(e) => setAge(Number(e.target.value))}
          className="border px-2 py-1 rounded"
        />
        <select
          value={gender}
          onChange={(e) => setGender(e.target.value)}
          className="border px-2 py-1 rounded"
        >
          <option value="">Choose gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>
      <button
        onClick={handleSave}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        save information
      </button>
    </div>
  );
}
