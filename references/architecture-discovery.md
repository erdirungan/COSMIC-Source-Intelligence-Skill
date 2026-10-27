# DISCOVER_ARCHITECTURE

1. Discover scope with `get_project_overview` (if pinned project), `list_repos`, `get_repo`; save publication and checkout revisions separately.
2. For each indexed repository, orient with `get_architecture`, `get_graph_schema`, `get_library_dependencies`; use `get_repo_overview` only for descriptive context.
3. For cross-repository calls, `get_project_map` reports **confirmed** path matches and **ambiguous** matches; it is PARTIAL and its missing edges do not prove isolation. Query `get_endpoint` and source locations with `get_snippet` when necessary.
4. Classify **deployed application, frontend app, integration runtime, library, module, logical package** separately. A Maven reactor module is not a deployable service unless build/deployment evidence demonstrates it.
5. Record edges with caller/provider, transport, paths/topic, data structures, source evidence, ambiguity and revision. Kafka producer/consumer direction differs from HTTP client/server: model separately.
6. APIs/interfaces are architectural evidence. Do not assign COSMIC movements or count them.
7. For missing or ambiguous runtime bindings, use `INFERRED`/`UNKNOWN`, not asserted deployment connections. Include unconnected members and coverage gaps.
8. Emit operation `DISCOVER_ARCHITECTURE` and put components/interfaces into `records` with typed records `component`/`interface`/`dependency`.
