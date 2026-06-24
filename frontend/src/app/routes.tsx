import { createBrowserRouter, Outlet } from "react-router";
import { Layout } from "./components/Layout";
import { Home } from "./pages/Home";
import { JDAnalysis } from "./pages/JDAnalysis";
import { Candidates } from "./pages/Candidates";
import { Leaderboard } from "./pages/Leaderboard";
import { Fairness } from "./pages/Fairness";
import { Health } from "./pages/Health";
import { CandidateDetails } from "./pages/CandidateDetails";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: Home },
      { path: "jd-analysis", Component: JDAnalysis },
      { path: "candidates", Component: Candidates },
      { path: "candidates/:id", Component: CandidateDetails },
      { path: "leaderboard", Component: Leaderboard },
      { path: "fairness", Component: Fairness },
      { path: "health", Component: Health },
    ],
  },
]);
