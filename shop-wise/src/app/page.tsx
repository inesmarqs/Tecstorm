import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen w-full" style={{ backgroundColor: "#0f1d1c" }}>
      <img src="/Design sem nome-4.png" alt="Home Image" className="w-3/4 max-w-md" style={{maxWidth:"23rem", maxHeight:"30rem",marginLeft:"2rem",marginTop:"4rem"}} />
      <nav className="nav bottom primary">
          <Link href="/login">START</Link>
        </nav>
    </div>
  );
}
