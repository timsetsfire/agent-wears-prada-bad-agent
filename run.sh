#!/bin/bash

# Root / structlog level for langgraph_api (default is INFO). --server-log-level only
# affects uvicorn + langgraph_api.server, not the rest of the stack.
export LOG_LEVEL="${LOG_LEVEL:-WARNING}"

env

langgraph dev --config ./agents.json --no-browser --host 0.0.0.0 --server-log-level WARNING