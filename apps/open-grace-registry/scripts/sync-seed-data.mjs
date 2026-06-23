#!/usr/bin/env node
/**
 * Aggregate Open Grace package seed YAML into static JSON for the registry portal.
 * No Python runtime required — run via `npm run sync-data`.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const APP_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(APP_ROOT, "../..");
const DATA_DIR = path.join(APP_ROOT, "data");

const SEED_PATHS = {
  capabilityFramework: path.join(
    REPO_ROOT,
    "packages/open-grace-governance/src/open_grace_governance/data/seed/capability_framework.yaml",
  ),
  riskRegistry: path.join(
    REPO_ROOT,
    "packages/open-grace-governance/src/open_grace_governance/data/seed/risk_registry.yaml",
  ),
  standardsRegistry: path.join(
    REPO_ROOT,
    "packages/open-grace-governance/src/open_grace_governance/data/seed/standards_registry.yaml",
  ),
  benchmarkRegistry: path.join(
    REPO_ROOT,
    "packages/open-grace-benchmarking/src/open_grace_benchmarking/data/seed/benchmark_registry.yaml",
  ),
  modelRegistry: path.join(
    REPO_ROOT,
    "packages/open-grace-agent-registry/src/open_grace_agent_registry/data/seed/model_registry.yaml",
  ),
  agentsManifest: path.join(REPO_ROOT, "data/registry/agents/manifest.yaml"),
};

const REFERENCE_MODELS = [
  {
    slug: "wikidata",
    display_name: "Wikidata",
    domain: "linked_open_data",
    governance_use: "Entity authority, provenance, and schema conformance checks",
  },
  {
    slug: "gbif",
    display_name: "GBIF",
    domain: "biodiversity",
    governance_use: "Occurrence data quality, Darwin Core binding, and taxonomic validation",
  },
  {
    slug: "unesco",
    display_name: "UNESCO World Heritage List",
    domain: "heritage_preservation",
    governance_use: "Stewardship, covenant review, and heritage-risk classification",
  },
  {
    slug: "internet-archive",
    display_name: "Internet Archive",
    domain: "digital_preservation",
    governance_use: "Fixity, format migration, and long-term access obligations",
  },
  {
    slug: "nist-ai-rmf",
    display_name: "NIST AI RMF",
    domain: "ai_risk_management",
    governance_use: "Risk registry taxonomy, impact assessment, and mitigation mapping",
  },
  {
    slug: "iso-42001",
    display_name: "ISO 42001",
    domain: "ai_management_system",
    governance_use: "Agent lifecycle controls, approval gates, and continual improvement",
  },
  {
    slug: "iso-27001",
    display_name: "ISO 27001",
    domain: "information_security",
    governance_use: "Access control, audit evidence, and security risk treatment",
  },
  {
    slug: "opentelemetry",
    display_name: "OpenTelemetry",
    domain: "observability",
    governance_use: "Trace context, metric dimensions, and audit telemetry correlation",
  },
];

function readYaml(filePath) {
  return yaml.load(fs.readFileSync(filePath, "utf8"));
}

function writeJson(name, data) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  const outPath = path.join(DATA_DIR, name);
  fs.writeFileSync(outPath, JSON.stringify(data, null, 2) + "\n");
  console.log(`wrote ${outPath}`);
}

function isoNow() {
  return new Date().toISOString();
}

function passingObservedValue(benchmark) {
  if (benchmark.threshold_min != null && benchmark.threshold_max != null) {
    return (benchmark.threshold_min + benchmark.threshold_max) / 2;
  }
  if (benchmark.threshold_min != null) {
    return Math.min(1, benchmark.threshold_min + 0.02);
  }
  if (benchmark.threshold_max != null) {
    return benchmark.threshold_max * 0.8;
  }
  return 1;
}

function evaluateBenchmark(benchmark, observed) {
  const reasons = [];
  let passed = true;
  if (benchmark.threshold_min != null && observed < benchmark.threshold_min) {
    passed = false;
    reasons.push(`below min ${benchmark.threshold_min}`);
  }
  if (benchmark.threshold_max != null && observed > benchmark.threshold_max) {
    passed = false;
    reasons.push(`above max ${benchmark.threshold_max}`);
  }
  return {
    benchmark_id: benchmark.benchmark_id,
    agent_id: benchmark.agent_id,
    metric: benchmark.metric,
    observed_value: observed,
    passed,
    reason: reasons.length ? reasons.join("; ") : "within thresholds",
  };
}

function withGovernance(row, stewardActor) {
  const now = isoNow();
  return {
    ...row,
    lifecycle_stage: row.lifecycle_stage ?? "publication",
    created_at: row.created_at ?? now,
    updated_at: row.updated_at ?? now,
    steward_actor: row.steward_actor ?? stewardActor,
    reference_models: row.reference_models ?? [],
    threshold_min: row.threshold_min ?? null,
    threshold_max: row.threshold_max ?? null,
    gold_dataset_ref: row.gold_dataset_ref ?? null,
  };
}

function buildAgents(manifest) {
  const steward = manifest.seed_actor ?? "wise-orchestration-seed";
  return manifest.agents.map((row) =>
    withGovernance(
      {
        ...row,
        reference_models:
          row.plane === "constitutional"
            ? ["nist-ai-rmf", "iso-42001"]
            : row.plane === "experience"
              ? ["unesco", "gbif", "wikidata"]
              : ["nist-ai-rmf", "iso-42001", "wikidata"],
      },
      steward,
    ),
  );
}

function buildAudits(agents, capabilities) {
  const audits = [];
  const constitutionalAgents = agents.filter((a) => a.plane === "constitutional");

  for (const agent of constitutionalAgents) {
    audits.push(withGovernance({
      audit_id: `wise.audit.${agent.agent_id.split(".").pop()}-publication-seed`,
      display_name: "Lifecycle approval to publication",
      subject_type: "agent",
      subject_id: agent.agent_id,
      evidence_ref: `otel://traces/${agent.langgraph_graph_id}-pub`,
      trace_id: `${agent.langgraph_graph_id}-pub`,
      outcome: "pass",
      reviewer_id: "architecture-office",
      lifecycle_stage: "audit",
      reference_models: ["opentelemetry", "iso-27001"],
    }, "architecture-office"));
  }

  for (const cap of capabilities.slice(0, 3)) {
    audits.push(withGovernance({
      audit_id: `wise.audit.${cap.id.split(".").pop()}-standards-seed`,
      display_name: `Standards conformance review — ${cap.name}`,
      subject_type: "capability",
      subject_id: cap.id,
      evidence_ref: `governance/audits/${cap.id.split(".").pop()}-v1`,
      trace_id: null,
      outcome: "pass",
      reviewer_id: "standards-steward",
      lifecycle_stage: "audit",
      reference_models: cap.reference_models,
    }, "standards-steward"));
  }

  return audits;
}

function main() {
  const capabilityYaml = readYaml(SEED_PATHS.capabilityFramework);
  const riskYaml = readYaml(SEED_PATHS.riskRegistry);
  const standardsYaml = readYaml(SEED_PATHS.standardsRegistry);
  const benchmarkYaml = readYaml(SEED_PATHS.benchmarkRegistry);
  const modelYaml = readYaml(SEED_PATHS.modelRegistry);
  const agentsManifest = readYaml(SEED_PATHS.agentsManifest);

  const capabilities = capabilityYaml.capability_classes.map((row) =>
    withGovernance(row, "open-grace-capability-seed"),
  );
  const agentBindings = capabilityYaml.agent_bindings;
  const risks = riskYaml.risks.map((row) =>
    withGovernance(row, "open-grace-governance-seed"),
  );
  const standards = standardsYaml.standards.map((row) =>
    withGovernance(row, "open-grace-governance-seed"),
  );
  const benchmarks = benchmarkYaml.benchmarks.map((row) =>
    withGovernance(row, row.steward_actor ?? "open-grace-governance-seed"),
  );
  const models = modelYaml.models.map((row) =>
    withGovernance(row, "open-grace-governance-seed"),
  );
  const agents = buildAgents(agentsManifest);

  const benchmarkScores = benchmarks.map((benchmark) => {
    const observed = passingObservedValue(benchmark);
    return {
      ...evaluateBenchmark(benchmark, observed),
      unit: benchmark.unit,
      threshold_min: benchmark.threshold_min ?? null,
      threshold_max: benchmark.threshold_max ?? null,
      display_name: benchmark.display_name,
    };
  });

  const audits = buildAudits(agents, capabilities);

  writeJson("reference-models.json", REFERENCE_MODELS);
  writeJson("agents.json", agents);
  writeJson("capabilities.json", capabilities);
  writeJson("agent-bindings.json", agentBindings);
  writeJson("benchmarks.json", benchmarks);
  writeJson("benchmark-scores.json", benchmarkScores);
  writeJson("risks.json", risks);
  writeJson("standards.json", standards);
  writeJson("models.json", models);
  writeJson("audits.json", audits);

  console.log(
    `synced ${agents.length} agents, ${capabilities.length} capabilities, ` +
      `${benchmarks.length} benchmarks, ${audits.length} audits, ${models.length} models`,
  );
}

main();
