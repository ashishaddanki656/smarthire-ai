import { useEffect, useState } from "react";
import { Link } from "react-router";
import { motion, AnimatePresence } from "motion/react";
import { Filter, Star, Briefcase, ChevronRight, CheckCircle2, Loader2 } from "lucide-react";
import { DisplayCandidate, getCandidates } from "../api";
import { Card, Button, Badge } from "../components/ui/shared";
import { ScoreRing } from "../components/ui/data-viz";

export function Candidates() {
  const [filter, setFilter] = useState("All");
  const [candidates, setCandidates] = useState<DisplayCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getCandidates()
      .then(setCandidates)
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load candidates"))
      .finally(() => setLoading(false));
  }, []);

  const visibleCandidates = candidates.filter((candidate) => {
    if (filter === "Top 10%") return candidate.rank <= Math.max(1, Math.ceil(candidates.length * 0.1));
    if (filter === "Open to Work") return candidate.activityScore >= 75;
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Candidate Discovery</h1>
          <p className="text-gray-400 mt-1">Top candidates matched using semantic FAISS retrieval.</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" className="gap-2">
            <Filter className="w-4 h-4" /> Filter
          </Button>
          <div className="bg-white/5 border border-white/10 rounded-lg p-1 flex">
            {["All", "Top 10%", "Open to Work"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                  filter === f ? "bg-white/10 text-white font-medium" : "text-gray-400 hover:text-white"
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>
      </div>

      {loading && (
        <Card className="flex items-center justify-center gap-3 text-gray-300">
          <Loader2 className="w-5 h-5 animate-spin text-[#06B6D4]" />
          Loading candidates from backend...
        </Card>
      )}

      {error && (
        <Card className="border-red-500/30 text-red-200">
          Backend connection failed. Start the FastAPI server and refresh. Details: {error}
        </Card>
      )}

      {!loading && !error && visibleCandidates.length === 0 && (
        <Card className="text-gray-300">No candidates found in the data folder.</Card>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <AnimatePresence>
          {visibleCandidates.map((candidate, idx) => (
            <motion.div
              key={candidate.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <Card glowOnHover className="h-full flex flex-col group p-0 relative overflow-visible">
                {candidate.rank === 1 && (
                  <div className="absolute -top-3 -right-3 z-10">
                    <div className="bg-gradient-to-r from-amber-400 to-amber-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow-[0_0_15px_rgba(245,158,11,0.5)] flex items-center gap-1">
                      <Star className="w-3 h-3 fill-current" /> Top Match
                    </div>
                  </div>
                )}
                
                <div className="p-6 pb-4 flex flex-col sm:flex-row gap-6 items-start sm:items-center border-b border-white/10">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-2xl font-bold text-white/20">#{candidate.rank}</span>
                      <h3 className="text-xl font-bold text-white">{candidate.name}</h3>
                      {candidate.githubActivity === "Very High" && (
                        <Badge variant="success" className="gap-1">
                          <CheckCircle2 className="w-3 h-3" /> Active Coder
                        </Badge>
                      )}
                    </div>
                    <div className="flex items-center gap-2 text-gray-400 text-sm mb-3">
                      <Briefcase className="w-4 h-4" />
                      {candidate.role} at <span className="text-gray-200">{candidate.company}</span>
                      <span className="text-white/20">•</span>
                      {candidate.experience}
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {candidate.skills.slice(0, 4).map(skill => (
                        <span key={skill} className="px-2 py-1 text-xs font-medium bg-white/5 border border-white/10 rounded text-gray-300">
                          {skill}
                        </span>
                      ))}
                      {candidate.skills.length > 4 && (
                        <span className="px-2 py-1 text-xs font-medium bg-white/5 border border-white/10 rounded text-gray-500">
                          +{candidate.skills.length - 4}
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex-shrink-0 bg-[#0B1220] rounded-xl p-3 border border-white/10 text-center shadow-inner">
                    <div className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-br from-[#6366F1] to-[#06B6D4]">
                      {candidate.finalScore.toFixed(1)}
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider font-bold mt-1">Final Score</div>
                  </div>
                </div>

                <div className="p-6 bg-black/20 flex-1 flex flex-col justify-between gap-6 rounded-b-xl">
                  <div className="flex justify-between px-2">
                    <ScoreRing score={candidate.semanticScore} size={48} strokeWidth={4} label="Semantic" color="#6366F1" />
                    <ScoreRing score={candidate.skillScore} size={48} strokeWidth={4} label="Skill" color="#06B6D4" />
                    <ScoreRing score={candidate.careerScore} size={48} strokeWidth={4} label="Career" color="#F59E0B" />
                    <ScoreRing score={candidate.activityScore} size={48} strokeWidth={4} label="Activity" color="#22C55E" />
                  </div>
                  
                  <div className="flex justify-end pt-2">
                    <Link to={`/candidates/${candidate.id}`}>
                      <Button variant="ghost" className="group/btn text-[#6366F1]">
                        View Details
                        <ChevronRight className="w-4 h-4 ml-1 transition-transform group-hover/btn:translate-x-1" />
                      </Button>
                    </Link>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
