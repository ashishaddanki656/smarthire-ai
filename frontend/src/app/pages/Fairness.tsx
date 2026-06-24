import { motion } from "motion/react";
import { ShieldCheck, EyeOff, Scale, CheckCircle2, UserCircle2, ArrowDown } from "lucide-react";
import { Card, Badge } from "../components/ui/shared";

export function Fairness() {
  return (
    <div className="max-w-5xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="text-center space-y-4">
        <div className="inline-flex items-center justify-center p-3 bg-[#22C55E]/10 rounded-full mb-4">
          <ShieldCheck className="w-10 h-10 text-[#22C55E]" />
        </div>
        <h1 className="text-4xl font-bold text-white">Fairness-Aware Ranking</h1>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          Our ethical AI pipeline removes demographic and referral metadata before evaluating pure capability.
        </p>
      </div>

      <Card className="p-8 md:p-12 border-[#22C55E]/30 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-6 opacity-10">
          <Scale className="w-64 h-64 text-[#22C55E]" />
        </div>
        
        <div className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
          {/* Step 1: Raw Data */}
          <div className="flex flex-col items-center text-center space-y-4">
            <h3 className="text-lg font-bold text-white">1. Raw Candidate Data</h3>
            <div className="bg-white/5 border border-white/10 rounded-xl p-4 w-full text-left space-y-2 relative">
              <div className="text-sm text-gray-300 flex items-center gap-2"><UserCircle2 className="w-4 h-4"/> name: John Doe</div>
              <div className="text-sm text-red-400 bg-red-400/10 px-2 py-1 rounded">employee_id: 8492</div>
              <div className="text-sm text-red-400 bg-red-400/10 px-2 py-1 rounded">referred_by: Jane S.</div>
              <div className="text-sm text-red-400 bg-red-400/10 px-2 py-1 rounded">referral_flag: true</div>
              <div className="text-sm text-gray-300">experience: 8 years</div>
              <div className="text-sm text-gray-300">skills: [Python, ML]</div>
            </div>
          </div>

          {/* Step 2: Bias Removal */}
          <div className="flex flex-col items-center justify-center space-y-4">
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <ArrowDown className="w-8 h-8 text-gray-500 hidden md:block rotate-[-90deg]" />
              <ArrowDown className="w-8 h-8 text-gray-500 md:hidden" />
            </motion.div>
            
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="bg-[#22C55E]/20 border border-[#22C55E]/50 rounded-full w-32 h-32 flex flex-col items-center justify-center shadow-[0_0_30px_rgba(34,197,94,0.3)] relative"
            >
              <EyeOff className="w-10 h-10 text-[#22C55E] mb-2" />
              <span className="text-xs font-bold text-[#22C55E] text-center px-2">Blind Engine</span>
              
              {/* Particle effect representing metadata being stripped */}
              <motion.div
                className="absolute inset-0 rounded-full border-2 border-dashed border-red-500/50"
                animate={{ rotate: 360 }}
                transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
              />
            </motion.div>
            
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
            >
              <ArrowDown className="w-8 h-8 text-gray-500 hidden md:block rotate-[-90deg]" />
              <ArrowDown className="w-8 h-8 text-gray-500 md:hidden" />
            </motion.div>
          </div>

          {/* Step 3: Pure Ranking */}
          <div className="flex flex-col items-center text-center space-y-4">
            <h3 className="text-lg font-bold text-white">2. Semantic Ranking</h3>
            <div className="bg-[#6366F1]/10 border border-[#6366F1]/30 rounded-xl p-4 w-full text-left space-y-2">
              <div className="text-sm text-gray-400 italic">Metadata stripped</div>
              <div className="text-sm text-gray-300">experience: 8 years</div>
              <div className="text-sm text-gray-300">skills: [Python, ML]</div>
              <div className="h-px w-full bg-white/10 my-2" />
              <div className="text-sm font-bold text-[#06B6D4] flex justify-between">
                Semantic Match <span>98%</span>
              </div>
              <div className="text-sm font-bold text-[#6366F1] flex justify-between">
                Final Score <span>94.5</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-12 p-4 bg-white/5 rounded-xl border border-white/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <h4 className="font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-[#22C55E]" />
              Metadata Revealed After Ranking
            </h4>
            <p className="text-sm text-gray-400 mt-1">Normal and referred candidates follow the identical evaluation pipeline.</p>
          </div>
          <Badge variant="success" className="text-lg px-4 py-2">Fairness Score: 99.8%</Badge>
        </div>
      </Card>
    </div>
  );
}
