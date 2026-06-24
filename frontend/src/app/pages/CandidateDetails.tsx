import { useEffect, useMemo, useState } from "react";
import { useParams, Link } from "react-router";
import { ArrowLeft, GitCommit, GraduationCap, MapPin, Mail, Award, BrainCircuit, CheckCircle2, Loader2 } from "lucide-react";
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Tooltip as RechartsTooltip } from "recharts";
import { DisplayCandidate, getCandidates } from "../api";
import { Card, Badge, Button } from "../components/ui/shared";
import { ProgressBar, ScoreRing } from "../components/ui/data-viz";
import { motion } from "motion/react";

export function CandidateDetails() {
  const { id } = useParams();
  const [candidates, setCandidates] = useState<DisplayCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getCandidates()
      .then(setCandidates)
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load candidates"))
      .finally(() => setLoading(false));
  }, []);

  const candidate = candidates.find(c => c.id === id) || candidates[0];
  const radarData = useMemo(() => candidate ? [
    { subject: 'Semantic Match', A: candidate.semanticScore, fullMark: 100 },
    { subject: 'Skill Depth', A: candidate.skillScore, fullMark: 100 },
    { subject: 'Career Growth', A: candidate.careerScore, fullMark: 100 },
    { subject: 'Activity', A: candidate.activityScore, fullMark: 100 },
    { subject: 'Education', A: candidate.education === "Not specified" ? 45 : 85, fullMark: 100 },
  ] : [], [candidate]);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <Card className="flex items-center justify-center gap-3 text-gray-300">
          <Loader2 className="w-5 h-5 animate-spin text-[#06B6D4]" />
          Loading candidate from backend...
        </Card>
      </div>
    );
  }

  if (error || !candidate) {
    return (
      <div className="max-w-6xl mx-auto space-y-4">
        <Link to="/candidates" className="inline-flex items-center text-sm text-gray-400 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to Candidates
        </Link>
        <Card className="border-red-500/30 text-red-200">
          Candidate data could not be loaded. {error}
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <Link to="/candidates" className="inline-flex items-center text-sm text-gray-400 hover:text-white transition-colors">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to Candidates
      </Link>

      <div className="flex flex-col lg:flex-row gap-8 items-start">
        {/* Left Column - Profile & Radar */}
        <div className="w-full lg:w-1/3 space-y-6">
          <Card className="flex flex-col items-center text-center p-8">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-[#6366F1] to-[#06B6D4] p-1 mb-4 shadow-[0_0_20px_rgba(99,102,241,0.3)]">
              <div className="w-full h-full rounded-full bg-[#0B1220] flex items-center justify-center text-3xl font-bold">
                {candidate.name.charAt(0)}
              </div>
            </div>
            <h1 className="text-2xl font-bold text-white mb-1">{candidate.name}</h1>
            <p className="text-[#06B6D4] font-medium mb-4">{candidate.role}</p>
            
            <div className="flex flex-wrap justify-center gap-2 mb-6">
              <Badge variant="default" className="gap-1"><MapPin className="w-3 h-3" /> {candidate.location}</Badge>
              <Badge variant="default" className="gap-1"><GraduationCap className="w-3 h-3" /> {candidate.experience}</Badge>
            </div>

            <div className="w-full space-y-3 text-sm">
              <div className="flex justify-between items-center py-2 border-b border-white/5">
                <span className="text-gray-400 flex items-center gap-2"><GitCommit className="w-4 h-4"/> GitHub</span>
                <span className="font-medium text-white">{candidate.githubActivity}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-white/5">
                <span className="text-gray-400 flex items-center gap-2"><Mail className="w-4 h-4"/> Reply Rate</span>
                <span className="font-medium text-white">{candidate.responseRate}</span>
              </div>
            </div>
            
            <Button className="w-full mt-6 gap-2"><Award className="w-4 h-4" /> Move to Interview</Button>
          </Card>

          <Card>
            <h3 className="text-lg font-semibold text-white mb-4">Competency Radar</h3>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                  <PolarGrid stroke="rgba(255,255,255,0.1)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#9ca3af', fontSize: 12 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                  <Radar name="Candidate" dataKey="A" stroke="#6366F1" fill="#6366F1" fillOpacity={0.3} />
                  <RechartsTooltip contentStyle={{ backgroundColor: '#0B1220', borderColor: 'rgba(255,255,255,0.1)' }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>

        {/* Right Column - Deep Dive */}
        <div className="w-full lg:w-2/3 space-y-6">
          <Card>
            <h2 className="text-xl font-bold text-white mb-4">Professional Summary</h2>
            <p className="text-gray-300 leading-relaxed">{candidate.summary}</p>
          </Card>

          <Card className="border-[#6366F1]/30 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-1 h-full bg-[#6366F1]" />
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
              <BrainCircuit className="w-5 h-5 text-[#6366F1]" />
              Explainable AI Reasoning
            </h2>
            
            <div className="bg-black/20 rounded-lg p-4 mb-6 flex items-center gap-4 border border-white/5">
              <div className="flex-shrink-0">
                <ScoreRing score={candidate.finalScore} size={80} strokeWidth={8} color="#06B6D4" />
              </div>
              <div>
                <h4 className="text-lg font-medium text-white">Highly Recommended</h4>
                <p className="text-sm text-gray-400 mt-1">
                  AI confidence is very high based on intersecting signals from semantic extraction and historical activity.
                </p>
              </div>
            </div>

            <div className="space-y-4">
              {candidate.reasoning.map((reason, i) => (
                <motion.div 
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 + 0.3 }}
                  className="flex items-start gap-3 bg-white/5 p-3 rounded-lg border border-white/5"
                >
                  <CheckCircle2 className="w-5 h-5 text-[#22C55E] shrink-0 mt-0.5" />
                  <span className="text-gray-200">{reason}</span>
                </motion.div>
              ))}
            </div>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <h3 className="text-lg font-semibold text-white mb-6">Score Breakdown</h3>
              <div className="space-y-5">
                <ProgressBar value={candidate.semanticScore} label="Semantic Match" color="#6366F1" />
                <ProgressBar value={candidate.skillScore} label="Skill Depth" color="#06B6D4" />
                <ProgressBar value={candidate.careerScore} label="Career Trajectory" color="#F59E0B" />
                <ProgressBar value={candidate.activityScore} label="Behavioral Activity" color="#22C55E" />
              </div>
            </Card>

            <Card>
              <h3 className="text-lg font-semibold text-white mb-4">Top Skills</h3>
              <div className="flex flex-wrap gap-2">
                {candidate.skills.map((skill) => (
                  <div key={skill} className="px-3 py-1.5 bg-white/5 border border-white/10 rounded-md text-sm text-gray-300">
                    {skill}
                  </div>
                ))}
              </div>
              
              <div className="mt-8">
                <h3 className="text-lg font-semibold text-white mb-4">Education</h3>
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-white/5 rounded-lg">
                    <GraduationCap className="w-5 h-5 text-gray-400" />
                  </div>
                  <div>
                    <p className="font-medium text-white">{candidate.education.split(",")[0]}</p>
                    <p className="text-sm text-gray-400">{candidate.education.split(",")[1] || "From candidate data"}</p>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
