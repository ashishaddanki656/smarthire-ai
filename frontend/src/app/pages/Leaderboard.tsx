import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { Trophy, Medal, Loader2 } from "lucide-react";
import { DisplayCandidate, getCandidates } from "../api";
import { Card, Badge } from "../components/ui/shared";

export function Leaderboard() {
  const [candidates, setCandidates] = useState<DisplayCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getCandidates()
      .then(setCandidates)
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load leaderboard"))
      .finally(() => setLoading(false));
  }, []);

  const top3 = candidates.slice(0, 3);

  return (
    <div className="max-w-7xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-amber-500/10 rounded-xl">
          <Trophy className="w-8 h-8 text-amber-500" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-white">Global Leaderboard</h1>
          <p className="text-gray-400">Real-time ranking across all analyzed talent pools.</p>
        </div>
      </div>

      {loading && (
        <Card className="flex items-center justify-center gap-3 text-gray-300">
          <Loader2 className="w-5 h-5 animate-spin text-[#06B6D4]" />
          Loading leaderboard from backend...
        </Card>
      )}

      {error && (
        <Card className="border-red-500/30 text-red-200">
          Backend connection failed. Start the FastAPI server and refresh. Details: {error}
        </Card>
      )}

      {!loading && !error && candidates.length === 0 && (
        <Card className="text-gray-300">No candidate rows found in data/candidates.csv.</Card>
      )}

      {!loading && !error && candidates.length > 0 && (
        <>
      {/* Podium */}
      <div className="flex flex-col md:flex-row items-end justify-center gap-4 md:gap-8 h-auto md:h-80 pt-10 border-b border-white/10 pb-10">
        {/* 2nd Place */}
        {top3[1] && (
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="order-2 md:order-1 flex flex-col items-center w-full md:w-1/4"
        >
          <div className="text-center mb-4">
            <h3 className="font-bold text-white text-lg">{top3[1].name}</h3>
            <p className="text-sm text-gray-400">{top3[1].finalScore.toFixed(1)}</p>
          </div>
          <div className="w-full h-32 bg-gradient-to-t from-gray-300/20 to-gray-300/5 rounded-t-xl border-t border-x border-gray-300/30 flex justify-center pt-4 relative overflow-hidden">
            <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.1)_50%,transparent_75%)] bg-[length:250%_250%,100%_100%] animate-[shimmer_2s_infinite]" />
            <span className="text-4xl font-black text-gray-400 opacity-50">2</span>
          </div>
        </motion.div>
        )}

        {/* 1st Place */}
        {top3[0] && (
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          className="order-1 md:order-2 flex flex-col items-center w-full md:w-1/3"
        >
          <Medal className="w-12 h-12 text-amber-400 mb-2 drop-shadow-[0_0_15px_rgba(251,191,36,0.8)]" />
          <div className="text-center mb-4">
            <h3 className="font-bold text-white text-xl">{top3[0].name}</h3>
            <Badge variant="warning" className="mt-1">{top3[0].finalScore.toFixed(1)} Match</Badge>
          </div>
          <div className="w-full h-48 bg-gradient-to-t from-amber-500/20 to-amber-500/5 rounded-t-xl border-t border-x border-amber-500/50 flex justify-center pt-4 shadow-[0_-10px_30px_rgba(245,158,11,0.2)] relative overflow-hidden">
            <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.2)_50%,transparent_75%)] bg-[length:250%_250%,100%_100%] animate-[shimmer_2s_infinite]" />
            <span className="text-5xl font-black text-amber-500 opacity-80">1</span>
          </div>
        </motion.div>
        )}

        {/* 3rd Place */}
        {top3[2] && (
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="order-3 md:order-3 flex flex-col items-center w-full md:w-1/4"
        >
          <div className="text-center mb-4">
            <h3 className="font-bold text-white text-lg">{top3[2].name}</h3>
            <p className="text-sm text-gray-400">{top3[2].finalScore.toFixed(1)}</p>
          </div>
          <div className="w-full h-24 bg-gradient-to-t from-amber-700/20 to-amber-700/5 rounded-t-xl border-t border-x border-amber-700/30 flex justify-center pt-4 relative overflow-hidden">
             <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.05)_50%,transparent_75%)] bg-[length:250%_250%,100%_100%] animate-[shimmer_2s_infinite]" />
            <span className="text-3xl font-black text-amber-700 opacity-50">3</span>
          </div>
        </motion.div>
        )}
      </div>

      {/* Table */}
      <Card className="p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-white/5 border-b border-white/10 text-xs uppercase tracking-wider text-gray-400">
                <th className="p-4 font-medium">Rank</th>
                <th className="p-4 font-medium">Candidate</th>
                <th className="p-4 font-medium">Final Score</th>
                <th className="p-4 font-medium">Semantic</th>
                <th className="p-4 font-medium">Skill</th>
                <th className="p-4 font-medium">Career</th>
                <th className="p-4 font-medium">Activity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {candidates.map((c, i) => (
                <motion.tr 
                  key={c.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: i * 0.1 }}
                  className="hover:bg-white/5 transition-colors group"
                >
                  <td className="p-4">
                    <span className={`font-bold ${i < 3 ? 'text-amber-400' : 'text-gray-500'}`}>
                      #{c.rank}
                    </span>
                  </td>
                  <td className="p-4">
                    <div className="font-medium text-white">{c.name}</div>
                    <div className="text-xs text-gray-400">{c.role}</div>
                  </td>
                  <td className="p-4">
                    <span className="inline-flex items-center justify-center px-2 py-1 rounded bg-[#6366F1]/20 text-[#6366F1] font-bold text-sm">
                      {c.finalScore.toFixed(1)}
                    </span>
                  </td>
                  <td className="p-4 text-sm text-gray-300">{c.semanticScore}</td>
                  <td className="p-4 text-sm text-gray-300">{c.skillScore}</td>
                  <td className="p-4 text-sm text-gray-300">{c.careerScore}</td>
                  <td className="p-4 text-sm text-gray-300">{c.activityScore}</td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
        </>
      )}
    </div>
  );
}
