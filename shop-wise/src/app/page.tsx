import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen w-full" style={{ backgroundColor: "#0f1d1c" }}>
      <nav className="nav bottom primary">
          <Link href="/login">START</Link>
        </nav>
    </div>
  );
}
