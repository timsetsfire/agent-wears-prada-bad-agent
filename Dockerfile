# Build from repo root: docker build -f agents/Dockerfile .
FROM python:3.11-slim

WORKDIR /app

# Install deps in their own layer so edits under agents/ do not invalidate pip cache.
COPY agents/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /tmp/pip-unpack-* /tmp/pip-metadata-* 2>/dev/null || true

COPY agents/ /app/
COPY synthetic-data/ /synthetic-data/

RUN chmod +x /app/run.sh
RUN chmod 777 -R /app 
RUN mkdir /.phoenix && chmod 777 /.phoenix

# ENTRYPOINT ["langgraph", "dev", "--config", "./agents.json", "--no-browser", "--host", "0.0.0.0", "--port", "8080"]
ENTRYPOINT ["/app/run.sh"]

# docker push timdatarobot/whoami