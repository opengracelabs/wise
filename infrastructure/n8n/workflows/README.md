# n8n workflow stubs

Importable skeleton workflows for WISE daily operations. Each file is valid n8n JSON with documented node intent; extend node parameters and credentials in the n8n UI after import.

| File | Workflow ID | Schedule (UTC) |
|------|-------------|----------------|
| `01-daily-discovery-run.json` | `wise-daily-discovery-run` | `0 2 * * *` |
| `02-daily-harvest-jobs.json` | `wise-daily-harvest-jobs` | `30 2 * * *` |
| `03-daily-quality-report.json` | `wise-daily-quality-report` | `0 6 * * *` |
| `04-daily-benchmark-report.json` | `wise-daily-benchmark-report` | `0 7 * * 1` (weekly) |
| `05-steward-approval-notifications.json` | `wise-steward-approval-notifications` | `*/30 * * * *` |
| `06-ci-failure-escalation.json` | `wise-ci-failure-escalation` | Webhook (GitHub) |

Full specifications: [`docs/implementation/n8n-workflow-catalog.md`](../../../docs/implementation/n8n-workflow-catalog.md).
