export type LifecycleStage =
  | "proposal"
  | "review"
  | "benchmark"
  | "approval"
  | "publication"
  | "audit"
  | "retirement";

export interface GovernedRecord {
  lifecycle_stage: LifecycleStage;
  created_at: string;
  updated_at: string;
  steward_actor: string | null;
  reference_models: string[];
}

export interface AgentRecord extends GovernedRecord {
  agent_id: string;
  spec_prefix: string;
  spec_path: string;
  display_name: string;
  plane: "platform" | "experience" | "constitutional";
  build_phase: number | null;
  service_binding: string | null;
  langgraph_graph_id: string;
  output_schema_uri: string;
  evidence_profile: boolean;
  read_only: boolean;
}

export interface CapabilityRecord extends GovernedRecord {
  id: string;
  name: string;
  description: string;
  owner: string;
  benchmark_set: string[];
  risk_profile: string[];
  approved_models: string[];
  required_standards: string[];
  audit_requirements: string[];
}

export interface AgentBinding {
  agent_id: string;
  capability_class_id: string;
}

export interface BenchmarkRecord extends GovernedRecord {
  benchmark_id: string;
  display_name: string;
  agent_id: string;
  metric: "accuracy" | "cost" | "latency" | "safety" | "reliability";
  threshold_min: number | null;
  threshold_max: number | null;
  unit: string;
  gold_dataset_ref?: string | null;
}

export interface BenchmarkScore {
  benchmark_id: string;
  agent_id: string;
  metric: string;
  observed_value: number;
  passed: boolean;
  reason: string;
  unit: string;
  threshold_min: number | null;
  threshold_max: number | null;
  display_name: string;
}

export interface RiskRecord extends GovernedRecord {
  risk_id: string;
  display_name: string;
  severity: "low" | "medium" | "high" | "critical";
  framework: string;
  control_id: string;
  mitigation: string;
  agent_id?: string;
  capability_id?: string;
}

export interface StandardRecord extends GovernedRecord {
  standard_id: string;
  display_name: string;
  binding_uri: string;
  schema_family: string;
  conformance_level: string;
  reference_model_slug: string;
}

export interface ModelRecord extends GovernedRecord {
  model_id: string;
  provider: string;
  model_name: string;
  council_role: string | null;
  allowed_planes: string[];
  safety_tier: "standard" | "elevated" | "restricted";
}

export interface AuditRecord extends GovernedRecord {
  audit_id: string;
  display_name: string;
  subject_type: "agent" | "capability" | "model" | "benchmark" | "standard";
  subject_id: string;
  evidence_ref: string;
  trace_id: string | null;
  outcome: "pass" | "fail" | "conditional";
  reviewer_id: string | null;
}

export interface ReferenceModelProfile {
  slug: string;
  display_name: string;
  domain: string;
  governance_use: string;
}

export interface RegistryData {
  agents: AgentRecord[];
  capabilities: CapabilityRecord[];
  agentBindings: AgentBinding[];
  benchmarks: BenchmarkRecord[];
  benchmarkScores: BenchmarkScore[];
  risks: RiskRecord[];
  standards: StandardRecord[];
  models: ModelRecord[];
  audits: AuditRecord[];
  referenceModels: ReferenceModelProfile[];
  executions: ExecutionRecord[];
  benchmarkRuns: BenchmarkRunRecord[];
}

export type ExecutionStatus = "pending" | "running" | "completed" | "failed" | "blocked";

export interface GateResult {
  gate_name: string;
  passed: boolean;
  errors: string[];
}

export interface ExecutionRecord {
  run_id: string;
  agent_id: string;
  model_id: string | null;
  capability_class_ids: string[];
  status: ExecutionStatus;
  started_at: string;
  completed_at: string | null;
  gate_results: GateResult[];
  output_ref: string | null;
  audit_id: string | null;
}

export interface BenchmarkRunRecord {
  benchmark_run_id: string;
  run_id: string;
  agent_id: string;
  capability_class_id: string;
  benchmark_id: string;
  passed: boolean;
  observed_value: number;
  reason: string;
  recorded_at: string;
}
