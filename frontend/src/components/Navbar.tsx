import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-blue-600 sticky top-0 z-20 text-white px-4 py-2 flex gap-12">
      <Link href="/">Home</Link>
      <Link href="/ask">Ask Question</Link>
      <Link href="/analyze">Analyze Report</Link>
      <Link href="/history">History</Link>
    </nav>
  );
}
