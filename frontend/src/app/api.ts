const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type ApiCandidate = Record<string, unknown>;

export type DisplayCandidate = {
  id: string;
  rank: number;
  name: string;
  role: string;
  experience: string;
  company: string;
  semanticScore: number;
  skillScore: number;
  careerScore: number;
  activityScore: number;
  finalScore: number;
  skills: string[];
  summary: string;
  reasoning: string[];
  githubActivity: string;
  responseRate: string;
  education: string;
  location: string;
};

export type Job = {
  id: string;
  role: string;
  skills: string;
  experience: number;
  education: string;
  seniority: string;
};

export type HealthResponse = {
  status: string;
  service: string;
  version: string;
};

export async function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export async function getJobs(): Promise<Job[]> {
  const response = await request<{ jobs: Job[] }>("/jobs");
  return response.jobs;
}

export async function parseJobDescription(jd: string) {
  return request<{
    role: string;
    skills: string[];
    experience: number;
    education: string;
    seniority?: string;
    certifications: string[];
  }>("/parse-jd", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jd }),
  });
}

export async function getCandidates(): Promise<DisplayCandidate[]> {
  const response = await request<{ candidates: ApiCandidate[] }>("/candidates");
  return normalizeCandidates(response.candidates);
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function normalizeCandidates(candidates: ApiCandidate[]): DisplayCandidate[] {
  return candidates
    .map(toDisplayCandidate)
    .sort((a, b) => b.finalScore - a.finalScore)
    .map((candidate, index) => ({ ...candidate, rank: index + 1 }));
}

function toDisplayCandidate(candidate: ApiCandidate, index: number): DisplayCandidate {
  const skills = splitList(candidate.skills);
  const experienceYears = toNumber(candidate.experience);
  const activity = toScore(candidate.activity_score ?? candidate.profile_completeness_score, 0.82);
  const skillScore = Math.min(100, 45 + skills.length * 9);
  const careerScore = Math.min(100, 50 + experienceYears * 7 + splitList(candidate.certifications).length * 6);
  const semanticScore = Math.min(100, Math.round((skillScore * 0.58) + (careerScore * 0.32) + 8));
  const finalScore = Math.round((semanticScore * 0.4 + skillScore * 0.3 + careerScore * 0.2 + activity * 100 * 0.1) * 10) / 10;

  return {
    id: String(candidate.id ?? `cand_${index + 1}`),
    rank: index + 1,
    name: String(candidate.name ?? "Unknown Candidate"),
    role: String(candidate.current_title ?? candidate.headline ?? inferRole(skills)),
    experience: `${experienceYears} ${experienceYears === 1 ? "year" : "years"}`,
    company: String(candidate.current_company ?? "Candidate Dataset"),
    semanticScore,
    skillScore,
    careerScore,
    activityScore: Math.round(activity * 100),
    finalScore,
    skills,
    summary: buildSummary(candidate, skills, experienceYears),
    reasoning: buildReasoning(candidate, skills, experienceYears),
    githubActivity: activity >= 0.9 ? "Very High" : activity >= 0.75 ? "High" : "Medium",
    responseRate: formatPercent(candidate.recruiter_response_rate, "80%"),
    education: String(candidate.education ?? "Not specified"),
    location: String(candidate.location ?? candidate.country ?? "Not specified"),
  };
}

function splitList(value: unknown): string[] {
  if (Array.isArray(value)) {
    return value.map(String).map((item) => item.trim()).filter(Boolean);
  }

  if (value === null || value === undefined) {
    return [];
  }

  const text = String(value).trim();
  if (!text || text.toLowerCase() === "none") {
    return [];
  }

  return text.split(",").map((item) => item.trim().replace(/^['"]|['"]$/g, "")).filter(Boolean);
}

function toNumber(value: unknown): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function toScore(value: unknown, fallback: number): number {
  const parsed = toNumber(value);
  if (!parsed) return fallback;
  return parsed > 1 ? Math.min(parsed / 100, 1) : Math.min(parsed, 1);
}

function inferRole(skills: string[]): string {
  const lowerSkills = skills.map((skill) => skill.toLowerCase());
  if (lowerSkills.some((skill) => skill.includes("react") || skill.includes("node"))) return "Frontend Developer";
  if (lowerSkills.some((skill) => skill.includes("kubernetes") || skill.includes("aws"))) return "Cloud Engineer";
  if (lowerSkills.some((skill) => skill.includes("machine") || skill.includes("tensorflow"))) return "Data Scientist";
  return "Software Engineer";
}

function buildSummary(candidate: ApiCandidate, skills: string[], experienceYears: number): string {
  if (candidate.summary) {
    return String(candidate.summary);
  }

  const skillText = skills.length ? skills.slice(0, 4).join(", ") : "core engineering skills";
  return `${candidate.name ?? "This candidate"} has ${experienceYears} years of experience with ${skillText}. Profile data is loaded from the project data folder through the backend API.`;
}

function buildReasoning(candidate: ApiCandidate, skills: string[], experienceYears: number): string[] {
  const certifications = splitList(candidate.certifications);
  const projects = splitList(candidate.projects);

  return [
    `${skills.length || "Multiple"} relevant skills found in the candidate data.`,
    `${experienceYears} years of experience available for career fit scoring.`,
    certifications.length ? `${certifications.length} certification signal(s) included.` : "No certification bias applied when scoring.",
    projects.length ? "Project history is available for review." : "Ranking is based on available structured profile fields.",
  ];
}

function formatPercent(value: unknown, fallback: string): string {
  const parsed = toNumber(value);
  if (!parsed) return fallback;
  return `${Math.round(parsed > 1 ? parsed : parsed * 100)}%`;
}
