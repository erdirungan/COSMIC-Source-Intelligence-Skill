# COSMIC constraints: facts vs measurement decisions

The skill extracts evidence, not COSMIC function points. The active CWB Measurement Context defines purpose, scope, software piece, layer, boundary and functional users.

- An API call, Java method call, database query or frontend state update is **not** automatically a COSMIC data movement.
- If CSR frontend and Marvel backend share a whole-application boundary, their HTTP interaction is internal. If measured as distinct software pieces, the same interface can be relevant at a component boundary. Do not double count inter-component movements during whole-size aggregation.
- Classify a proposed data group by the **Object of Interest whose attributes it conveys**, not the operation name, DTO class name, endpoint, table, or transport.
- An Entry/Exit/Read/Write needs functional-user / persistent-storage semantics within the active context. It cannot be assigned in a context-free source extraction.
- One DTO can contain multiple candidate OOIs; many SQL statements need not mean many Reads. A database table may be a mere association, lookup, localization or implementation table.
- Do not assume a subscription response contains product name/logo because a UI shows them; inspect actual payload, transformations, catalog enrichment and evidence.
- Keep separate canonical **technical architecture evidence**, **functional behavior evidence**, **candidate business concepts**, and **context-specific measurement proposals**. Only the first three belong to this skill's output.
- State VERIFIED_SOURCE / VERIFIED_INDEX / INFERRED / UNKNOWN separately. Attach evidence and raise unresolved questions rather than manufacturing facts.
