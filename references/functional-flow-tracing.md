# TRACE_FUNCTIONAL_FLOW

1. Identify actual trigger: human action, event, timer, or software user. Do not equate route activation with a proven preceding click.
2. Follow frontend route/resolver/state/action/service, transport contract, backend controller/service, repositories and response construction using `get_endpoint`, `search_code`, `get_symbol_context`, `get_snippet` and, if warranted, `get_project_map`. Use `get_task_context` for broad scoping, not bundled `ask` queries.
3. For each ordered interaction store source and destination **technical** components, call/response contract, fields/provenance, conditions, confidence and source range.
4. For attributes, track `DECLARED`, `POPULATED`, `TRANSMITTED` (if verified), `CONSUMED` and `DISPLAYED` as distinct facts, not one boolean. Type declarations do not establish serialized values.
5. Inspect conditional branches and errors. Trace UI-emitted events and whether an action actually calls an API; don't invent hidden network calls.
6. Check transformations and DTO mismatches. Darwin regression: frontend `serviceAddress: string` versus `.addrDesc` read and backend Address type remains unresolved without transformation evidence.
7. Keep technical sequence independent of COSMIC sequence; neither internal calls nor database statements are auto-counted.
8. Return `records[]` typed `functionalFlow`, `interaction`, `attributeLineage`, plus `unresolvedQuestions` for missing routing, runtime endpoints, data ownership or UI behavior.
