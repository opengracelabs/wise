import { describe, expect, it } from "vitest";
import {
  evaluateBenchmark,
  evaluateCapabilityBenchmarks,
  getAgent,
  getBenchmarkScore,
  getCapabilitiesForAgent,
  loadRegistryData,
} from "./data";

describe("loadRegistryData", () => {
  it("loads all registry collections", () => {
    const data = loadRegistryData();
    expect(data.agents.length).toBeGreaterThan(0);
    expect(data.capabilities.length).toBe(8);
    expect(data.benchmarks.length).toBeGreaterThan(0);
    expect(data.models.length).toBe(5);
    expect(data.audits.length).toBeGreaterThan(0);
    expect(data.referenceModels.some((r) => r.slug === "wikidata")).toBe(true);
    expect(data.referenceModels.some((r) => r.slug === "gbif")).toBe(true);
    expect(data.referenceModels.some((r) => r.slug === "unesco")).toBe(true);
  });

  it("resolves agent by id", () => {
    const agent = getAgent("wise.agent.standards");
    expect(agent?.display_name).toBe("Standards Agent");
    expect(agent?.read_only).toBe(true);
  });

  it("resolves capability bindings for benchmark agent", () => {
    const caps = getCapabilitiesForAgent("wise.agent.benchmark");
    const ids = caps.map((c) => c.id);
    expect(ids).toContain("wise.capability.class.coding");
    expect(ids).toContain("wise.capability.class.research");
  });

  it("includes benchmark scores that pass thresholds", () => {
    const score = getBenchmarkScore("wise.benchmark.translation-quality");
    expect(score).toBeDefined();
    expect(score?.passed).toBe(true);
  });
});

describe("evaluateBenchmark", () => {
  it("flags values below threshold_min", () => {
    const data = loadRegistryData();
    const benchmark = data.benchmarks.find(
      (b) => b.benchmark_id === "wise.benchmark.translation-quality",
    )!;
    const result = evaluateBenchmark(benchmark, 0.5);
    expect(result.passed).toBe(false);
    expect(result.reason).toContain("below min");
  });

  it("flags values above threshold_max", () => {
    const data = loadRegistryData();
    const benchmark = data.benchmarks.find(
      (b) => b.benchmark_id === "wise.benchmark.translation-cost",
    )!;
    const result = evaluateBenchmark(benchmark, 0.2);
    expect(result.passed).toBe(false);
    expect(result.reason).toContain("above max");
  });
});

describe("evaluateCapabilityBenchmarks", () => {
  it("passes translation capability when scores are present", () => {
    const data = loadRegistryData();
    const capability = data.capabilities.find((c) => c.id === "wise.capability.class.translation")!;
    const result = evaluateCapabilityBenchmarks(capability, data.benchmarkScores);
    expect(result.passed).toBe(true);
    expect(result.evaluations.length).toBe(2);
  });
});
