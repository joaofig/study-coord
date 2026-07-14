from pathlib import Path
from src.tools.singleton import singleton


def get_script(script_name: str) -> str:
    path = Path("src/db/sql") / script_name
    return path.read_text(
        encoding="utf-8"
    )


@singleton
class SQLCache:
    def __init__(self):
        self.cache = {}

    def get(self, query_key: str) -> str:
        if query_key not in self.cache:
            self.cache[query_key] = get_script(query_key)
        sql = str(self.cache[query_key])
        return sql

    def clear(self):
        self.cache.clear()
