from dotenv import load_dotenv
load_dotenv()

from metrics import make_metrics_ctx, log_usage, _get_collection
from config import CONFIG

print("MONGODB_URI host:", __import__("os").environ["MONGODB_URI"].split("@")[-1].split("/")[0])
print("db_name:", CONFIG["mongodb"]["db_name"])
print("metrics collection_name:", CONFIG["metrics"]["collection_name"])

ctx = make_metrics_ctx(chunking_strategy="recursive", retrieval_strategy="hybrid", run_id="diagnostic")
log_usage("gemini-2.5-flash", "generate", 1.0, ctx, input_tokens=10, output_tokens=10)

col = _get_collection()
print("Total docs in collection right now:", col.count_documents({}))
print("Most recent doc:", col.find_one(sort=[("timestamp", -1)]))