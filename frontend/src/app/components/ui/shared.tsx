import React from "react";
import { motion, HTMLMotionProps } from "motion/react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface CardProps extends HTMLMotionProps<"div"> {
  glass?: boolean;
  glowOnHover?: boolean;
}

export function Card({ className, glass = true, glowOnHover = false, children, ...props }: CardProps) {
  return (
    <motion.div
      whileHover={glowOnHover ? { y: -5, boxShadow: "0 0 20px rgba(99, 102, 241, 0.2)" } : undefined}
      className={cn(
        "rounded-xl p-6 relative overflow-hidden transition-all duration-300",
        glass ? "glass-panel" : "bg-white/5 border border-white/10",
        className
      )}
      {...props}
    >
      {children}
    </motion.div>
  );
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
}

export function Button({ className, variant = "primary", size = "md", children, ...props }: ButtonProps) {
  const baseStyles = "inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus:outline-none disabled:opacity-50 disabled:pointer-events-none";
  const variants = {
    primary: "bg-[#6366F1] hover:bg-[#4F46E5] text-white shadow-[0_0_15px_rgba(99,102,241,0.3)] hover:shadow-[0_0_20px_rgba(99,102,241,0.5)] border border-[#6366F1]/50",
    secondary: "bg-[#06B6D4]/10 hover:bg-[#06B6D4]/20 text-[#06B6D4] border border-[#06B6D4]/50 shadow-[0_0_15px_rgba(6,182,212,0.1)]",
    outline: "border border-white/20 hover:bg-white/5 text-gray-200",
    ghost: "hover:bg-white/10 text-gray-300 hover:text-white"
  };
  const sizes = {
    sm: "px-3 py-1.5 text-xs",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base"
  };

  return (
    <button className={cn(baseStyles, variants[variant], sizes[size], className)} {...props}>
      {children}
    </button>
  );
}

export function Badge({ children, className, variant = "default" }: { children: React.ReactNode, className?: string, variant?: "default"|"success"|"warning"|"primary"|"secondary" }) {
  const variants = {
    default: "bg-white/10 text-gray-300 border border-white/10",
    success: "bg-[#22C55E]/10 text-[#22C55E] border border-[#22C55E]/20 shadow-[0_0_10px_rgba(34,197,94,0.2)]",
    warning: "bg-amber-500/10 text-amber-400 border border-amber-500/20",
    primary: "bg-[#6366F1]/10 text-[#6366F1] border border-[#6366F1]/20 shadow-[0_0_10px_rgba(99,102,241,0.2)]",
    secondary: "bg-[#06B6D4]/10 text-[#06B6D4] border border-[#06B6D4]/20",
  };
  return (
    <span className={cn("px-2.5 py-0.5 rounded-full text-xs font-medium inline-flex items-center", variants[variant], className)}>
      {children}
    </span>
  );
}
