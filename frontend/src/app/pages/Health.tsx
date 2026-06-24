import { useEffect, useState } from "react";
import { Activity, Server, Clock, Signal } from "lucide-react";
import { motion } from "motion/react";
import { getHealth, HealthResponse } from "../api";
import { Card } from "../components/ui/shared";

export function Health() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load health status"));
  }, []);

  const isHealthy = health?.status === "healthy";
  const services = [
    { service: health?.service ?? "SmartHire AI API", status: isHealthy ? "Operational" : "Unavailable", uptime: health ? "Online" : "Waiting", latency: health ? "Live" : "N/A" },
    { service: "Candidate CSV Loader", status: isHealthy ? "Ready" : "Waiting", uptime: "data/candidates.csv", latency: "Backend" },
    { service: "Jobs CSV Loader", status: isHealthy ? "Ready" : "Waiting", uptime: "data/jobs.csv", latency: "Backend" },
    { service: "JD Parser API", status: isHealthy ? "Ready" : "Waiting", uptime: health?.version ?? "N/A", latency: "/parse-jd" },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <Activity className="w-8 h-8 text-[#06B6D4]" /> System Health
        </h1>
        <p className="text-gray-400">Real-time status of backend microservices and AI pipelines.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Global Status", value: isHealthy ? "Backend Online" : "Checking", icon: Signal, color: isHealthy ? "text-[#22C55E]" : "text-amber-400" },
          { label: "API Version", value: health?.version ?? "N/A", icon: Clock, color: "text-white" },
          { label: "Service", value: health?.service ?? "FastAPI", icon: Server, color: "text-white" },
          { label: "Data Source", value: "CSV Files", icon: Activity, color: "text-[#06B6D4]" }
        ].map((stat, i) => (
          <Card key={i} className="flex items-center gap-4 p-6">
            <div className={`p-3 bg-white/5 rounded-lg border border-white/10 ${stat.color}`}>
              <stat.icon className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-gray-400">{stat.label}</p>
              <p className={`text-xl font-bold ${stat.color}`}>{stat.value}</p>
            </div>
          </Card>
        ))}
      </div>

      <Card className="p-0 overflow-hidden">
        <div className="p-6 border-b border-white/10 flex justify-between items-center bg-white/5">
          <h3 className="font-semibold text-white">Microservice Status</h3>
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <span className="flex h-2 w-2 rounded-full bg-[#22C55E] animate-pulse"></span>
            Auto-refreshing
          </div>
        </div>
        
        <div className="divide-y divide-white/5">
          {error && (
            <div className="p-6 text-red-200">
              Backend connection failed. Start the FastAPI server and refresh. Details: {error}
            </div>
          )}

          {services.map((service, i) => (
            <motion.div 
              key={service.service}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className="flex items-center justify-between p-6 hover:bg-white/5 transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#22C55E] opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-[#22C55E]"></span>
                </div>
                <div>
                  <h4 className="text-white font-medium">{service.service}</h4>
                  <p className="text-xs text-gray-500 mt-1">ID: srv-{Math.floor(Math.random() * 10000)}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-8">
                <div className="text-right hidden sm:block">
                  <p className="text-sm text-gray-400">Uptime</p>
                  <p className="font-medium text-white">{service.uptime}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-400">Latency</p>
                  <p className="font-medium text-white">{service.latency}</p>
                </div>
                <div className={`px-3 py-1 rounded text-sm font-medium w-28 text-center ${
                  isHealthy ? "bg-[#22C55E]/10 text-[#22C55E] border border-[#22C55E]/30" : "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                }`}>
                  {service.status}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </Card>
    </div>
  );
}
