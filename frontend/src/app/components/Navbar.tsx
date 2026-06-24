import { Link, useLocation } from "react-router";
import { BrainCircuit, Activity, ShieldCheck, Trophy, Users, FileText, Home } from "lucide-react";
import { motion } from "motion/react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const navItems = [
  { name: "Home", path: "/", icon: Home },
  { name: "JD Analysis", path: "/jd-analysis", icon: FileText },
  { name: "Candidates", path: "/candidates", icon: Users },
  { name: "Leaderboard", path: "/leaderboard", icon: Trophy },
  { name: "Fairness", path: "/fairness", icon: ShieldCheck },
  { name: "Health", path: "/health", icon: Activity },
];

export function Navbar() {
  const location = useLocation();

  return (
    <nav className="fixed top-0 w-full z-50 glass border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="relative">
              <BrainCircuit className="h-8 w-8 text-[#6366F1]" />
              <div className="absolute inset-0 bg-[#6366F1] blur-md opacity-50 rounded-full" />
            </div>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-[#6366F1]">
              SmartHire AI
            </span>
          </div>
          
          <div className="hidden md:block">
            <div className="flex items-baseline space-x-1">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path || (item.path !== "/" && location.pathname.startsWith(item.path));
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    className={cn(
                      "relative px-3 py-2 rounded-md text-sm font-medium transition-colors group flex items-center gap-2",
                      isActive ? "text-white" : "text-gray-400 hover:text-white hover:bg-white/5"
                    )}
                  >
                    <Icon className="w-4 h-4" />
                    {item.name}
                    {isActive && (
                      <motion.div
                        layoutId="navbar-indicator"
                        className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#06B6D4] shadow-[0_0_10px_#06B6D4]"
                        initial={false}
                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                  </Link>
                );
              })}
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-[#6366F1] to-[#06B6D4] p-[1px] cursor-pointer">
              <div className="h-full w-full bg-[#0B1220] rounded-full flex items-center justify-center">
                <span className="text-xs font-bold text-white">HR</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
