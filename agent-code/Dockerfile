# Build from repo root: docker build -f agents/Dockerfile .
FROM python:3.11-slim

WORKDIR /app

# Workloads API runs the container as a non-root, arbitrary UID with no
# /etc/passwd entry, so $HOME resolves to "/" and uv can't write its cache
# there. Point both at a world-writable path under /app instead.
ENV HOME=/app
ENV UV_CACHE_DIR=/app/.cache/uv

RUN pip3 install uv && uv init

# Install deps in their own layer so edits under agents/ do not invalidate pip cache.
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock
RUN uv sync

COPY . /app/

RUN chmod +x /app/run.sh
RUN chmod 777 -R /app 
RUN mkdir /.phoenix && chmod 777 /.phoenix

# ENTRYPOINT ["langgraph", "dev", "--config", "./agents.json", "--no-browser", "--host", "0.0.0.0", "--port", "8080"]
ENTRYPOINT ["/app/run.sh"]

# docker push timdatarobot/whoami