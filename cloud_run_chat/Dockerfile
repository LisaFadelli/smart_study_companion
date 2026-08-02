FROM python:3.11-slim

WORKDIR /app

# NOTE: build context = project root (smart_study_companion/), NOT this folder.
# All COPY paths below are relative to that root, not to this Dockerfile's location.
 
# Install deps first (layer caching): only re-run pip install if requirements.txt changes
COPY cloud_run_chat/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# App code: single canonical source per file, no duplication
COPY cloud_run_chat/main.py .
COPY rag_chain.py .
COPY store.py .
COPY config.py .
 
ENV PORT=8080
EXPOSE 8080
 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]