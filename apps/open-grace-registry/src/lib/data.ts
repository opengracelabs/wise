import type {
  AgentRecord,
  AuditRecord,
  BenchmarkRecord,
  BenchmarkScore,
  CapabilityRecord,
  ModelRecord,
  ReferenceModelProfile,
  RegistryData,
  RiskRecord,
  StandardRecord,
} from "./types";

import agents from "../../data/agents.json";
import capabilities from "../../data/capabilities.json";
import agentBindings from "../../data/agent-bindings.json";
import benchmarks from "../../data/benchmarks.json";
import benchmarkScores from "../../data/benchmark-scores.json";
import risks from "../../data/risks.json";
import standards from "../../data/standards.json";
import models from "../../data/models.json";
import audits from "../../data/audits.json";
import referenceModels from "../../data/reference-models.json";

let cache: RegistryData | null = null;

export function loadRegistryData(): RegistryData {
  if (cache) return cache;
  cache = {
    agents: agents as AgentRecord[],
    capabilities: capabilities as CapabilityRecord[],
    agentBindings: agentBindings as RegistryData["agentBindings"],
    benchmarks: benchmarks as BenchmarkRecord[],
    benchmarkScores: benchmarkScores as BenchmarkScore[],
    risks: risks as RiskRecord[],
    standards: standards as StandardRecord[],
    models: models as ModelRecord[],
    audits: audits as AuditRecord[],
    referenceModels: referenceModels as ReferenceModelProfile[],
  };
  return cache;
}

export function getAgent(id: string): AgentRecord | undefined {
  return loadRegistryData().agents.find((a) => a.agent_id === id);
}

export function getCapability(id: string): CapabilityRecord | undefined {
  return loadRegistryData().capabilities.find((c) => c.id === id);
}

export function getBenchmark(id: string): BenchmarkRecord | undefined {
  return loadRegistryData().benchmarks.find((b) => b.benchmark_id === id);
}

export function getAudit(id: string): AuditRecord | undefined {
  return loadRegistryData().audits.find((a) => a.audit_id === id);
}

export function getModel(id: string): ModelRecord | undefined {
  return loadRegistryData().models.find((m) => m.model_id === id);
}

export function getBenchmarkScore(benchmarkId: string): BenchmarkScore | undefined {
  return loadRegistryData().benchmarkScores.find((s) => s.benchmark_id === benchmarkId);
}

export function getAuditsForSubject(subjectId: string): AuditRecord[] {
  return loadRegistryData().audits.filter((a) => a.subject_id === subjectId);
}

export function getBenchmarksForAgent(agentId: string): BenchmarkRecord[] {
  return loadRegistryData().benchmarks.filter((b) => b.agent_id === agentId);
}

export function getBenchmarkScoresForAgent(agentId: string): BenchmarkScore[] {
  return loadRegistryData().benchmarkScores.filter((s) => s.agent_id === agentId);
}

export function getCapabilitiesForAgent(agentId: string): CapabilityRecord[] {
  const data = loadRegistryData();
  const classIds = data.agentBindings
    .filter((b) => b.agent_id === agentId)
    .map((b) => b.capability_class_id);
  return data.capabilities.filter((c) => classIds.includes(c.id));
}

export function getRisksForCapability(capability: CapabilityRecord): RiskRecord[] {
  return loadRegistryData().risks.filter((r) => capability.risk_profile.includes(r.risk_id));
}

export function getStandardsForCapability(capability: CapabilityRecord): StandardRecord[] {
  return loadRegistryData().standards.filter((s) =>
    capability.required_standards.includes(s.standard_id),
  );
}

export function getReferenceModel(slug: string): ReferenceModelProfile | undefined {
  return loadRegistryData().referenceModels.find((r) => r.slug === slug);
}

export function evaluateBenchmark(
  benchmark: BenchmarkRecord,
  observed: number,
): { passed: boolean; reason: string } {
  const reasons: string[] = [];
  let passed = true;
  if (benchmark.threshold_min != null && observed < benchmark.threshold_min) {
    passed = false;
    reasons.push(`below min ${benchmark.threshold_min}`);
  }
  if (benchmark.threshold_max != null && observed > benchmark.threshold_max) {
    passed = false;
    reasons.push(`above max ${benchmark.threshold_max}`);
  }
  return { passed, reason: reasons.length ? reasons.join("; ") : "within thresholds" };
}

export function evaluateCapabilityBenchmarks(
  capability: CapabilityRecord,
  scores: BenchmarkScore[],
): { passed: boolean; evaluations: BenchmarkScore[]; failures: string[] } {
  const data = loadRegistryData();
  const evaluations: BenchmarkScore[] = [];
  const failures: string[] = [];

  for (const benchmarkId of capability.benchmark_set) {
    const score = scores.find((s) => s.benchmark_id === benchmarkId);
    if (!score) {
      const def = data.benchmarks.find((b) => b.benchmark_id === benchmarkId);
      failures.push(`missing observed value for: ${benchmarkId}`);
      if (!def) failures.push(`missing benchmark definition: ${benchmarkId}`);
      continue;
    }
    evaluations.push(score);
    if (!score.passed) {
      failures.push(`${benchmarkId}: ${score.reason}`);
    }
  }

  return {
    passed: failures.length === 0 && evaluations.length === capability.benchmark_set.length,
    evaluations,
    failures,
  };
}
