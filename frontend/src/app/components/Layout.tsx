import { useEffect, useState } from "react";
import { Outlet } from "react-router";
import { Navbar } from "./Navbar";
import { motion } from "motion/react";

function MouseGlow() {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div
      className="pointer-events-none fixed inset-0 z-0 transition-opacity duration-300"
      style={{
        background: `radial-gradient(600px circle at ${position.x}px ${position.y}px, rgba(99, 102, 241, 0.08), transparent 40%)`,
      }}
    />
  );
}

function Particles() {
  return (
    <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
      {[...Array(30)].map((_, i) => {
        const size = Math.random() * 3 + 1;
        return (
          <motion.div
            key={i}
            className="absolute rounded-full bg-[#06B6D4]/20"
            style={{
              width: size,
              height: size,
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -100, 0],
              opacity: [0.1, 0.5, 0.1],
              scale: [1, 1.5, 1],
            }}
            transition={{
              duration: Math.random() * 10 + 10,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        );
      })}
    </div>
  );
}

export function Layout() {
  return (
    <div className="min-h-screen bg-[#0B1220] text-gray-100 flex flex-col relative selection:bg-[#6366F1]/30">
      <MouseGlow />
      <Particles />
      <Navbar />
      <main className="flex-1 relative z-10 pt-16 mt-8 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <Outlet />
      </main>
    </div>
  );
}
