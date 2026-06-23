export interface SearchFilterOptions {
  query?: string;
  lifecycleStage?: string;
  plane?: string;
  severity?: string;
  outcome?: string;
  referenceModel?: string;
}

function normalize(value: string): string {
  return value.toLowerCase().trim();
}

function matchesQuery(fields: (string | null | undefined)[], query: string): boolean {
  const q = normalize(query);
  if (!q) return true;
  return fields.some((field) => field && normalize(field).includes(q));
}

export function filterAgents<
  T extends {
    agent_id: string;
    display_name: string;
    plane: string;
    lifecycle_stage: string;
    reference_models: string[];
    service_binding?: string | null;
  },
>(items: T[], options: SearchFilterOptions): T[] {
  return items.filter((item) => {
    if (options.lifecycleStage && item.lifecycle_stage !== options.lifecycleStage) return false;
    if (options.plane && item.plane !== options.plane) return false;
    if (options.referenceModel && !item.reference_models.includes(options.referenceModel)) {
      return false;
    }
    if (
      options.query &&
      !matchesQuery(
        [item.agent_id, item.display_name, item.plane, item.service_binding],
        options.query,
      )
    ) {
      return false;
    }
    return true;
  });
}

export function filterCapabilities<
  T extends {
    id: string;
    name: string;
    description: string;
    owner: string;
    lifecycle_stage: string;
    reference_models: string[];
  },
>(items: T[], options: SearchFilterOptions): T[] {
  return items.filter((item) => {
    if (options.lifecycleStage && item.lifecycle_stage !== options.lifecycleStage) return false;
    if (options.referenceModel && !item.reference_models.includes(options.referenceModel)) {
      return false;
    }
    if (
      options.query &&
      !matchesQuery([item.id, item.name, item.description, item.owner], options.query)
    ) {
      return false;
    }
    return true;
  });
}

export function filterBenchmarks<
  T extends {
    benchmark_id: string;
    display_name: string;
    agent_id: string;
    metric: string;
    lifecycle_stage: string;
    reference_models: string[];
  },
>(items: T[], options: SearchFilterOptions): T[] {
  return items.filter((item) => {
    if (options.lifecycleStage && item.lifecycle_stage !== options.lifecycleStage) return false;
    if (options.referenceModel && !item.reference_models.includes(options.referenceModel)) {
      return false;
    }
    if (
      options.query &&
      !matchesQuery([item.benchmark_id, item.display_name, item.agent_id, item.metric], options.query)
    ) {
      return false;
    }
    return true;
  });
}

export function filterAudits<
  T extends {
    audit_id: string;
    display_name: string;
    subject_id: string;
    subject_type: string;
    outcome: string;
    lifecycle_stage: string;
    reviewer_id?: string | null;
  },
>(items: T[], options: SearchFilterOptions): T[] {
  return items.filter((item) => {
    if (options.lifecycleStage && item.lifecycle_stage !== options.lifecycleStage) return false;
    if (options.outcome && item.outcome !== options.outcome) return false;
    if (
      options.query &&
      !matchesQuery(
        [item.audit_id, item.display_name, item.subject_id, item.reviewer_id],
        options.query,
      )
    ) {
      return false;
    }
    return true;
  });
}

export function filterModels<
  T extends {
    model_id: string;
    model_name: string;
    provider: string;
    council_role?: string | null;
    lifecycle_stage: string;
    reference_models: string[];
    safety_tier: string;
  },
>(items: T[], options: SearchFilterOptions): T[] {
  return items.filter((item) => {
    if (options.lifecycleStage && item.lifecycle_stage !== options.lifecycleStage) return false;
    if (options.referenceModel && !item.reference_models.includes(options.referenceModel)) {
      return false;
    }
    if (
      options.query &&
      !matchesQuery(
        [item.model_id, item.model_name, item.provider, item.council_role, item.safety_tier],
        options.query,
      )
    ) {
      return false;
    }
    return true;
  });
}

export function filterRisks<
  T extends {
    risk_id: string;
    display_name: string;
    severity: string;
    framework: string;
    mitigation: string;
    lifecycle_stage: string;
  },
>(items: T[], options: SearchFilterOptions): T[] {
  return items.filter((item) => {
    if (options.severity && item.severity !== options.severity) return false;
    if (options.lifecycleStage && item.lifecycle_stage !== options.lifecycleStage) return false;
    if (
      options.query &&
      !matchesQuery(
        [item.risk_id, item.display_name, item.framework, item.mitigation],
        options.query,
      )
    ) {
      return false;
    }
    return true;
  });
}

export function uniqueValues<T>(items: T[], accessor: (item: T) => string): string[] {
  return [...new Set(items.map(accessor))].sort();
}
