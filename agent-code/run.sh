#!/bin/bash

# Root / structlog level for langgraph_api (default is INFO). --server-log-level only
# affects uvicorn + langgraph_api.server, not the rest of the stack.
export LOG_LEVEL="${LOG_LEVEL:-WARNING}"



uv run langgraph dev --config ./agent.json --no-browser --host 0.0.0.0 --server-log-level WARNING
# langgraph dev --config ./agent.json docker