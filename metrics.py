"""
metrics.py

Environments supported:
  - local (your laptop)
  - Cloud Functions (GCP) -- detected via K_SERVICE env var

Pricing:
- Gemini 2.5 Flash:
    - input:  $0.30 / 1M tokens
    - output: $2.50 / 1M tokens
- Vertex AI text-embedding-004 (per character):
    - online: $0.000025 / 1,000 chars
    - batch:  $0.00002  / 1,000 chars

Note:
- This is a pure side-channel: it does not change chain outputs or retrieval logic.
- Logging only happens if you pass a non-None metrics_ctx.
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pymongo import MongoClient

from config import CONFIG

def _get_deployment_context() -> str:
    """
    Auto-detect deployment_context:
      - 'cloud_function' if K_SERVICE is set
      - 'local' otherwise
    """
    if os.getenv("K_SERVICE"):
        return "cloud_function"
    return "local

_client=None
def _get_collection():
    """
    Same MONGODB_URI env var + connection pattern store.py already uses,
    just pointed at CONFIG["metrics"]["collection_name"] instead of a
    chunks_* collection. Client is cached at module level so repeated
    log_usage() calls in one process don't reopen a connection each time.
    """
    global _client
    if _client is None:
        _client = MongoClient(os.environ["MONGODB_URI"])
    db = _client.get_database(CONFIG["mongodb"]["db_name"])
    return db.get_collection(CONFIG["metrics"]["collection_name"])
 
 
def make_metrics_ctx(
    chunking_strategy: Optional[str] = None,
    retrieval_strategy: Optional[str] = None,
    run_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build the metrics_ctx dict that log_usage() expects. Call this once per
    chain/ingest run and pass the same dict into every log_usage() call for
    that run, so all events from one query or one ingestion job share the
    same run_id and get tagged with the same strategy labels.
 
    Defaults chunking_strategy/retrieval_strategy from CONFIG if not passed,
    so you don't have to repeat what's already set there.
    """
    return {
        "chunking_strategy": chunking_strategy or CONFIG["chunking"]["strategy"],
        "retrieval_strategy": retrieval_strategy or CONFIG["retrieval"]["strategy"],
        "run_id": run_id,
        "pricing": CONFIG["metrics"]["pricing"],
    }
 
 
def _compute_cost_usd(
    model: str,
    pricing: Dict[str, Any],
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    input_chars: Optional[int] = None,
) -> float:
    if model not in pricing:
        return 0.0
 
    p = pricing[model]
    cost = 0.0
 
    # Generation model (tokens)
    if "input_per_million" in p:
        in_tok = input_tokens or 0
        out_tok = output_tokens or 0
        cost = (
            in_tok * p["input_per_million"]
            + out_tok * p["output_per_million"]
        ) / 1_000_000.0
 
    # Embedding model (characters)
    if "embedding_rate_per_1k_chars" in p:
        chars = input_chars or 0
        rate_per_1k = p["embedding_rate_per_1k_chars"]
        cost = chars * (rate_per_1k / 1_000.0)
 
    return cost
 
 
def log_usage(
    model: str,
    component: str,
    latency_seconds: float,
    metrics_ctx: Dict[str, Any],
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    input_chars: Optional[int] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log a single usage event to the 'usage_metrics' collection.
 
    Parameters
    ----------
    model : str
        Model name, e.g. "gemini-2.5-flash", "text-embedding-005".
    component : str
        One of: "condense", "generate", "embed".
    latency_seconds : float
        How long the API call took (seconds).
    metrics_ctx : dict
        From make_metrics_ctx(): chunking_strategy, retrieval_strategy,
        run_id, pricing.
    input_tokens, output_tokens : int, optional
        For generation models.
    input_chars : int, optional
        For embedding models.
    extra : dict, optional
        Anything else worth tagging on this event, e.g. {"source": "file.pdf"}.
 
    Failures here are logged and swallowed rather than raised -- a Mongo
    hiccup on the telemetry write should never break the chain the user
    is waiting on.
    """
    pricing = metrics_ctx["pricing"]
    cost_usd = _compute_cost_usd(
        model=model,
        pricing=pricing,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        input_chars=input_chars,
    )
 
    deployment_context = _get_deployment_context()
 
    doc = {
        "model": model,
        "component": component,
        "latency_seconds": latency_seconds,
        "cost_usd": cost_usd,
        "chunking_strategy": metrics_ctx["chunking_strategy"],
        "retrieval_strategy": metrics_ctx["retrieval_strategy"],
        "deployment_context": deployment_context,
        "timestamp": datetime.now(timezone.utc),
    }
 
    if metrics_ctx.get("run_id"):
        doc["run_id"] = metrics_ctx["run_id"]
 
    if input_tokens is not None:
        doc["input_tokens"] = input_tokens
    if output_tokens is not None:
        doc["output_tokens"] = output_tokens
    if input_chars is not None:
        doc["input_chars"] = input_chars
 
    if extra:
        doc.update(extra)
 
    try:
        _get_collection().insert_one(doc)
    except Exception as e:
        print(f"[metrics] failed to log usage event ({component}/{model}): {e}")
 
 
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    # Smoke test -- confirms MONGODB_URI + collection access work before
    # wiring this into the real chain.
    ctx = make_metrics_ctx(chunking_strategy="recursive", retrieval_strategy="hybrid", run_id="smoke_test")
    log_usage("gemini-2.5-flash", "generate", 1.23, ctx, input_tokens=500, output_tokens=120)
    log_usage("text-embedding-005", "embed", 0.8, ctx, input_chars=4000, extra={"source": "smoke_test.pdf"})
    print("Logged 2 smoke-test events to usage_metrics.")