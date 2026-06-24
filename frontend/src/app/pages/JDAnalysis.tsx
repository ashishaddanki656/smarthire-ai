import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Search, Loader2, FileText, CheckCircle2, BrainCircuit } from "lucide-react";
import { getJobs, Job, parseJobDescription } from "../api";
import { Card, Button, Badge } from "../components/ui/shared";

export function JDAnalysis() {
  const [jdText, setJdText] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getJobs()
      .then((jobRows) => {
        setJobs(jobRows);
        if (jobRows[0]) {
          setJdText(formatJobDescription(jobRows[0]));
        }
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load jobs"));
  }, []);

  const handleAnalyze = async () => {
    if (!jdText.trim()) return;
    setAnalyzing(true);
    setResults(null);
    setError("");
    
    try {
      const parsed = await parseJobDescription(jdText);
      setResults({
        ...parsed,
        experience: `${parsed.experience}+ Years`,
        skills: parsed.skills.map((skill) => ({ name: skill, conf: 95 })),
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not analyze JD");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-white">Job Description Analysis</h1>
        <p className="text-gray-400">Paste your job description to extract core requirements and generate semantic embedding vectors.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card className="flex flex-col h-[600px] border-white/10 p-0">
          <div className="p-4 border-b border-white/10 bg-white/5 flex items-center gap-2">
            <FileText className="w-5 h-5 text-[#6366F1]" />
            <span className="font-semibold text-white">JD Editor</span>
          </div>
          <div className="p-4 flex-1 flex flex-col relative">
            {jobs.length > 0 && (
              <div className="mb-3 flex flex-wrap gap-2">
                {jobs.map((job) => (
                  <button
                    key={job.id}
                    onClick={() => setJdText(formatJobDescription(job))}
                    className="px-3 py-1.5 text-xs rounded-md bg-white/5 border border-white/10 text-gray-300 hover:text-white hover:bg-white/10"
                  >
                    {job.role}
                  </button>
                ))}
              </div>
            )}
            <textarea
              className="flex-1 w-full bg-transparent border-none resize-none focus:outline-none text-gray-300 leading-relaxed"
              placeholder="Paste the job description here..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
          </div>
          <div className="p-4 border-t border-white/10 bg-white/5 flex justify-end">
            <Button onClick={handleAnalyze} disabled={analyzing || !jdText.trim()}>
              {analyzing ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search className="w-4 h-4 mr-2" />
                  Extract Signals
                </>
              )}
            </Button>
          </div>
        </Card>

        <Card className="flex flex-col h-[600px] border-white/10 p-0 overflow-y-auto">
          <div className="p-4 border-b border-white/10 bg-white/5 flex items-center gap-2 sticky top-0 z-10 glass">
            <BrainCircuit className="w-5 h-5 text-[#06B6D4]" />
            <span className="font-semibold text-white">AI Extraction Panel</span>
          </div>
          
          <div className="p-6">
            {!results && !analyzing && (
              <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-4 pt-32">
                <Search className="w-12 h-12 opacity-20" />
                <p>{error ? `Backend error: ${error}` : "Waiting for JD analysis..."}</p>
              </div>
            )}

            {analyzing && (
              <div className="space-y-6 pt-10">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div key={i} className="flex flex-col gap-2">
                    <div className="h-4 bg-white/10 rounded w-1/4 animate-pulse" />
                    <div className="h-10 bg-white/5 rounded-lg w-full animate-pulse" />
                  </div>
                ))}
              </div>
            )}

            <AnimatePresence>
              {results && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-8"
                >
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1">
                      <span className="text-sm text-gray-400">Inferred Role</span>
                      <p className="text-lg font-semibold text-white">{results.role}</p>
                    </div>
                    <div className="space-y-1">
                      <span className="text-sm text-gray-400">Seniority</span>
                      <Badge variant="primary">{results.seniority}</Badge>
                    </div>
                    <div className="space-y-1">
                      <span className="text-sm text-gray-400">Required Experience</span>
                      <p className="text-white">{results.experience}</p>
                    </div>
                    <div className="space-y-1">
                      <span className="text-sm text-gray-400">Education</span>
                    <p className="text-white">{results.education}</p>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-sm font-medium text-gray-400 mb-3">Extracted Skills & Vectors</h3>
                    <div className="flex flex-wrap gap-2">
                      {results.skills.map((skill: any, idx: number) => (
                        <motion.div
                          key={skill.name}
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: idx * 0.1 }}
                          className="flex items-center gap-2 bg-[#6366F1]/10 border border-[#6366F1]/30 rounded-full px-3 py-1.5"
                        >
                          <span className="text-sm font-medium text-[#6366F1]">{skill.name}</span>
                          <span className="text-xs text-[#06B6D4] flex items-center gap-1">
                            <CheckCircle2 className="w-3 h-3" />
                            {skill.conf}% conf
                          </span>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="pt-4 border-t border-white/10">
                    <div className="bg-white/5 rounded-lg p-4 border border-white/10 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-white">Ready for Semantic Search</p>
                        <p className="text-xs text-gray-400 mt-1">Parsed by the backend JD API.</p>
                      </div>
                      <Button size="sm" variant="secondary">Run Query</Button>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </Card>
      </div>
    </div>
  );
}

function formatJobDescription(job: Job): string {
  return `${job.seniority} ${job.role}

Required skills: ${job.skills}
Experience: ${job.experience}+ years
Education: ${job.education}`;
}
