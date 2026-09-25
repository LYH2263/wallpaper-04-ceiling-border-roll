from app.db import connect

CEILING_SEGMENT_KEY = "ceiling_segment_len"
# 缺少设置项时的兜底默认段长（米/角），正常由 seed 写入、设置页维护。
DEFAULT_CEILING_SEGMENT_LEN = 0.5


def get_all() -> dict:
    conn = connect()
    try:
        return {r["key"]: r["value"] for r in conn.execute("SELECT key,value FROM settings").fetchall()}
    finally:
        conn.close()


def get_float(key: str, default: float | None = None) -> float | None:
    conn = connect()
    try:
        row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    finally:
        conn.close()
    if row is None or row["value"] is None or row["value"] == "":
        return default
    try:
        return float(row["value"])
    except (TypeError, ValueError):
        return default


def get_ceiling_segment_len() -> float:
    return get_float(CEILING_SEGMENT_KEY, DEFAULT_CEILING_SEGMENT_LEN)


def upsert(key: str, value) -> None:
    conn = connect()
    try:
        conn.execute(
            "INSERT INTO settings(key,value) VALUES (?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value)),
        )
        conn.commit()
    finally:
        conn.close()
