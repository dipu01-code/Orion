# ORION architecture assessment

## Current architecture

ORION is currently a small Python 3.10 command-line assistant. Its executable
entry point is `backend/main.py`, which waits for the wake word, accepts a text
command, and prints a response from `brain.core.OrionBrain`.

```text
CLI -> OrionBrain -> parser -> intent router -> tool registry -> local OS/tool
                       |                 |
                       +-> model fallback +-> formatted response
```

v0.2 adds a provider-neutral `models` package, persistent SQLite memory, and a
bounded model-driven tool loop:

```text
User input -> Brain -> SQLite context retrieval -> known intent/tool OR Model
           -> registered tool observation -> final model response -> memory write
```

## Existing capabilities

- Text wake-word conversation loop.
- Rule-based parsing for system information, arithmetic, application launch,
  new application windows, and creating a folder/opening it in an application.
- Safe AST-based arithmetic evaluation.
- System-information and macOS application-launching tools.
- A sequential, structured two-step plan for folder creation plus application
  launch.

## Entry points, packages, and dependencies

| Area | Location | Notes |
| --- | --- | --- |
| CLI | `backend/main.py` | Synchronous interactive loop |
| Cognition | `backend/brain/` | Parse, plan, execute, route, coordinate |
| Models | `backend/models/` | Provider-neutral `Model` contract; local fallback |
| Memory | `backend/memory/` | Contract and ephemeral in-process store |
| Tools | `backend/tools/` | Built-ins and legacy registry |
| Voice/config | `backend/voice/`, `backend/config/` | Empty placeholders |

`backend/requirements.txt` is empty: v0.2 uses only the Python standard
library. The OpenAI-compatible model adapter uses `ORION_MODEL_PROVIDER=openai`,
`OPENAI_API_KEY`, and `OPENAI_MODEL`; optional `OPENAI_BASE_URL`,
`ORION_MEMORY_DB`, and `ORION_SYSTEM_INSTRUCTION` control endpoint, memory
location, and personality. There are no package lockfiles or committed secrets.

## Current data flow and tools

`OrionBrain.process()` is the asynchronous central interface. It retrieves
matching working-memory records, writes the user input, dispatches recognised
commands through the existing router/tool registry, otherwise selects an
injected `Model` through `ModelRouter`, then records the response. `respond()` is retained solely for
the existing synchronous CLI.

Registered legacy tools are `system_info`, `open_application`,
`open_new_window`, `create_folder`, `open_folder_in_application`, and
`calculate`. `tools.base.Tool` / `ToolResult` define the forward-looking
standard interface; the legacy registry is deliberately preserved during this
first migration.

## What works and what is preserved

- Existing command grammar and result formatting remain in place.
- Existing calculator and planner are reused by the brain.
- The user-modified whitespace-only change in `backend/tools/registry.py` is
  untouched.
- The new local fallback makes unknown requests explicit instead of pretending
  to be an LLM; no network connection or API key is required.

## Gaps and architectural concerns

- Memory is process-local and uses transparent keyword matching only; it has no
  persistence, embeddings, user consent, summarisation, or sensitive-data
  policy.
- The legacy registry uses functions rather than the new `Tool` interface.
- Tool safety metadata is descriptive only. Folder creation defaults to the
  home directory and application tools can launch local applications without a
  permission/confirmation manager.
- There is no provider adapter, model routing policy, async tool execution,
  audit log, research/RAG/knowledge system, browser, terminal, git tool,
  tests for the old tools, or configuration schema.
- `TaskExecutor` is not yet wired into the main brain loop; the older router
  retains parallel execution logic.

## Proposed incremental migration

1. **Completed: foundation** — document the codebase; add brain, model, memory,
   and tool contracts; test the brain-model-memory-tool vertical slice.
2. **Next: safe tool boundary** — adapt each registry function to `Tool`, add
   action categories and a confirmation policy, then route every plan through
   `TaskExecutor` with structured observations.
3. **Then: durable memory** — add a local store, explicit user-memory consent,
   provenance, retention/deletion, and retrieval evaluation tests.
4. **Then: model adapters** — add configuration-backed local/cloud adapters and
   a policy-driven `ModelRouter`; keep provider SDK types outside `brain`.
5. **Later: knowledge and research** — introduce document ingestion, provenance
   metadata, retrieval/reranking, source verification, and research reports.

## Implemented in this slice

- `async OrionBrain.process(user_input)` coordination API.
- Replaceable `Model`, `ModelRequest`, and `ModelResponse` contracts.
- A deterministic `LocalFallbackModel` for offline development.
- `MemoryStore` and `MemoryRecord` contracts plus an in-memory implementation.
- `Tool` and `ToolResult` contract definitions.
- Unit tests covering model invocation, tool-backed arithmetic, and memory
  search/delete.

## Not implemented

Implemented in v0.2: an OpenAI-compatible provider adapter with safe network,
timeout, rate-limit, and invalid-response handling; persistent SQLite memory;
read-only file/project/Git inspection; registered model tool schemas; and a
three-step bounded tool-observation loop. Research, PDFs, voice, audit logging,
interactive approval handoff, filesystem writes, terminal commands, RAG,
knowledge graphs, and learning are intentionally **not implemented** yet.
