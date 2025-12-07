import time
from typing import Dict

class Metrics:
    def __init__(self):
        self.start_time = time.time()
        self.reset()

    def reset(self):
        self.data = {
            "rewrite_ms": [],
            "embed_ms": [],
            "search_ms": [],
            "rerank_ms": [],
            "prompt_ms": [],
            "llm_ms": [],
            "query_count": 0
        }

    def record(self, stage: str, duration_ms: float):
        if stage not in self.data:
            return
        self.data[stage].append(duration_ms)

    def increment_queries(self):
        self.data["query_count"] += 1

    def summary(self) -> Dict:
        def avg(arr):
            return sum(arr) / len(arr) if arr else 0

        return {
            "query_count": self.data["query_count"],
            "avg_rewrite_ms": avg(self.data["rewrite_ms"]),
            "avg_embed_ms": avg(self.data["embed_ms"]),
            "avg_search_ms": avg(self.data["search_ms"]),
            "avg_rerank_ms": avg(self.data["rerank_ms"]),
            "avg_prompt_ms": avg(self.data["prompt_ms"]),
            "avg_llm_ms": avg(self.data["llm_ms"]),
            "uptime_seconds": self.uptime_seconds(),
        }

    def uptime_seconds(self):
        return int(time.time() - self.start_time)

metrics = Metrics()
