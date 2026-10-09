# ORION

ORION is a modular, local-first desktop-assistant foundation. v0.2 provides a
provider-agnostic conversational brain, controlled model tool calling, and
SQLite-backed local memory while preserving the original command-line tools.

## Run

```bash
cd backend
export ORION_MODEL_PROVIDER=openai
export OPENAI_API_KEY='...'
export OPENAI_MODEL='gpt-4.1-mini'
python3 main.py
```

`OPENAI_BASE_URL` optionally selects a compatible endpoint. `ORION_MEMORY_DB`
sets the SQLite location (default: `orion_memory.sqlite3` in the working
directory). `ORION_SYSTEM_INSTRUCTION` customises the ORION personality.
Credentials are environment variables only and are never written to memory or
logs.

Without those model variables, built-in commands still work and conversational
requests return a clear configuration message.

## Safety

Models can access only registered tools. Read-only inspection, calculator, and
system-info tools run automatically; tools marked `caution` require approval
and are reported as such. This version does not expose unrestricted shell
execution to the model.

## Tests

```bash
cd backend
python3 -m unittest discover -s tests -v
```
