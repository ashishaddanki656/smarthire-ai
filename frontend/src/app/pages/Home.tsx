import { motion } from "motion/react";
import { Link } from "react-router";
import { ArrowRight, BrainCircuit, Search, Zap, Briefcase, Network, ShieldCheck, FileText, Activity } from "lucide-react";
import { Button, Card } from "../components/ui/shared";

function Hero() {
  return (
    <section className="relative py-20 lg:py-32 flex flex-col items-center text-center">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#6366F1]/20 rounded-full blur-[120px] pointer-events-none" />
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative z-10"
      >
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 mb-8 backdrop-blur-sm">
          <span className="flex h-2 w-2 rounded-full bg-[#06B6D4] animate-pulse"></span>
          <span className="text-sm font-medium text-gray-300">SmartHire Engine v4.0 Active</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
          <span className="text-white">SmartHire</span>{" "}
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#6366F1] to-[#06B6D4]">AI</span>
        </h1>
        
        <h2 className="text-xl md:text-3xl font-medium text-gray-300 mb-6 max-w-3xl mx-auto">
          Bias-Free Intelligent Candidate Discovery
        </h2>
        
        <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
          AI-powered candidate ranking using semantic search, FAISS retrieval, fairness-aware ranking and explainable AI.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link to="/jd-analysis">
            <Button size="lg" className="px-8 py-4 text-lg w-full sm:w-auto h-14">
              Upload Job Description
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
          <Link to="/candidates">
            <Button variant="secondary" size="lg" className="px-8 py-4 text-lg w-full sm:w-auto h-14">
              View Candidates
            </Button>
          </Link>
        </div>
      </motion.div>
    </section>
  );
}

const pipelineStages = [
  { id: "jd", label: "JD Parser", icon: FileText, color: "#94A3B8" },
  { id: "embed", label: "BGE Embedding", icon: BrainCircuit, color: "#6366F1" },
  { id: "faiss", label: "FAISS Search", icon: Search, color: "#06B6D4" },
  { id: "bias", label: "Bias Removal", icon: ShieldCheck, color: "#22C55E" },
  { id: "rank", label: "Signal Fusion", icon: Zap, color: "#F59E0B" },
  { id: "xai", label: "Explainable AI", icon: Network, color: "#EC4899" },
];

function ArchitecturePipeline() {
  return (
    <section className="py-20 border-t border-white/10 relative">
      <div className="text-center mb-16">
        <h3 className="text-3xl font-bold text-white mb-4">Architecture Pipeline</h3>
        <p className="text-gray-400">Intelligent flow from raw description to top candidate.</p>
      </div>

      <div className="relative max-w-5xl mx-auto overflow-x-auto pb-8">
        <div className="flex items-center justify-between min-w-[800px] px-8 relative">
          {/* Animated Connecting Line */}
          <div className="absolute top-1/2 left-16 right-16 h-0.5 bg-white/10 -translate-y-1/2 z-0 overflow-hidden">
             <motion.div 
               className="h-full w-1/3 bg-gradient-to-r from-transparent via-[#6366F1] to-transparent"
               animate={{ x: ["-100%", "300%"] }}
               transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
             />
          </div>

          {pipelineStages.map((stage, idx) => {
            const Icon = stage.icon;
            return (
              <div key={stage.id} className="relative z-10 flex flex-col items-center group">
                <motion.div 
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ delay: idx * 0.1 }}
                  whileHover={{ scale: 1.1, boxShadow: `0 0 20px ${stage.color}40` }}
                  className="w-16 h-16 rounded-2xl glass-panel flex items-center justify-center mb-4 cursor-pointer"
                  style={{ borderColor: `${stage.color}50` }}
                >
                  <Icon className="w-8 h-8" style={{ color: stage.color }} />
                  
                  {/* Tooltip */}
                  <div className="absolute -top-12 opacity-0 group-hover:opacity-100 transition-opacity bg-white/10 backdrop-blur-md px-3 py-1 rounded-lg border border-white/20 whitespace-nowrap text-sm pointer-events-none">
                    Processing Stage {idx + 1}
                  </div>
                </motion.div>
                <span className="text-sm font-medium text-gray-300">{stage.label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

const features = [
  { title: "Semantic Search", desc: "Beyond keywords. Understands intent and contextual matching.", icon: Search, color: "#6366F1" },
  { title: "Bias-Free Ranking", desc: "Strips demographic metadata before evaluating capability.", icon: ShieldCheck, color: "#22C55E" },
  { title: "Behavioral Intelligence", desc: "Analyzes GitHub, contributions, and response rates.", icon: Activity, color: "#06B6D4" },
  { title: "Career Intelligence", desc: "Models career trajectory and promotion velocity.", icon: Briefcase, color: "#F59E0B" },
  { title: "Explainable AI", desc: "Transparent reasoning for every single candidate rank.", icon: Network, color: "#EC4899" },
  { title: "FAISS Retrieval", desc: "Millisecond vector search across millions of profiles.", icon: Zap, color: "#8B5CF6" },
];

function Features() {
  return (
    <section className="py-20 border-t border-white/10">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((f, i) => {
          const Icon = f.icon;
          return (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              viewport={{ once: true }}
            >
              <Card glowOnHover className="h-full cursor-default group">
                <div 
                  className="w-12 h-12 rounded-lg flex items-center justify-center mb-4 bg-white/5 transition-colors group-hover:bg-white/10"
                >
                  <Icon className="w-6 h-6" style={{ color: f.color }} />
                </div>
                <h4 className="text-xl font-bold text-white mb-2">{f.title}</h4>
                <p className="text-gray-400 leading-relaxed">{f.desc}</p>
              </Card>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}

export function Home() {
  return (
    <div className="space-y-10">
      <Hero />
      <ArchitecturePipeline />
      <Features />
    </div>
  );
}
