import { describe, expect, it } from "vitest";
import {
  filterAgents,
  filterAudits,
  filterBenchmarks,
  filterCapabilities,
  filterModels,
  uniqueValues,
} from "./search";

const sampleAgents = [
  {
    agent_id: "wise.agent.standards",
    display_name: "Standards Agent",
    plane: "constitutional",
    lifecycle_stage: "publication",
    reference_models: ["nist-ai-rmf"],
    service_binding: "orchestrator-service",
  },
  {
    agent_id: "wise.agent.translation",
    display_name: "Translation Agent",
    plane: "platform",
    lifecycle_stage: "publication",
    reference_models: ["wikidata"],
    service_binding: "orchestrator-service",
  },
];

describe("filterAgents", () => {
  it("filters by query across id and display name", () => {
    const result = filterAgents(sampleAgents, { query: "translation" });
    expect(result).toHaveLength(1);
    expect(result[0].agent_id).toBe("wise.agent.translation");
  });

  it("filters by plane", () => {
    const result = filterAgents(sampleAgents, { plane: "constitutional" });
    expect(result).toHaveLength(1);
  });

  it("filters by reference model", () => {
    const result = filterAgents(sampleAgents, { referenceModel: "wikidata" });
    expect(result).toHaveLength(1);
  });
});

describe("filterCapabilities", () => {
  const capabilities = [
    {
      id: "wise.capability.class.research",
      name: "Research",
      description: "Research capability",
      owner: "Office",
      lifecycle_stage: "publication",
      reference_models: ["unesco", "gbif"],
    },
  ];

  it("matches description text", () => {
    const result = filterCapabilities(capabilities, { query: "research" });
    expect(result).toHaveLength(1);
  });
});

describe("filterBenchmarks", () => {
  const benchmarks = [
    {
      benchmark_id: "wise.benchmark.kg-reliability",
      display_name: "KG reliability",
      agent_id: "wise.agent.knowledge-graph",
      metric: "reliability",
      lifecycle_stage: "publication",
      reference_models: ["wikidata"],
    },
  ];

  it("filters by metric", () => {
    const result = filterBenchmarks(benchmarks, { query: "reliability" });
    expect(result).toHaveLength(1);
  });
});

describe("filterAudits", () => {
  const audits = [
    {
      audit_id: "wise.audit.standards-publication-seed",
      display_name: "Lifecycle approval",
      subject_id: "wise.agent.standards",
      subject_type: "agent",
      outcome: "pass",
      lifecycle_stage: "audit",
      reviewer_id: "architecture-office",
    },
  ];

  it("filters by outcome", () => {
    const result = filterAudits(audits, { outcome: "pass" });
    expect(result).toHaveLength(1);
    expect(filterAudits(audits, { outcome: "fail" })).toHaveLength(0);
  });
});

describe("filterModels", () => {
  const models = [
    {
      model_id: "wise.model.qwen-research",
      model_name: "qwen-max",
      provider: "alibaba",
      council_role: "research",
      lifecycle_stage: "publication",
      reference_models: ["gbif", "wikidata"],
      safety_tier: "standard",
    },
  ];

  it("filters by provider", () => {
    const result = filterModels(models, { query: "alibaba" });
    expect(result).toHaveLength(1);
  });
});

describe("uniqueValues", () => {
  it("returns sorted unique values", () => {
    const values = uniqueValues(sampleAgents, (a) => a.plane);
    expect(values).toEqual(["constitutional", "platform"]);
  });
});
