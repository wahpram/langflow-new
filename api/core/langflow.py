from functools import lru_cache
from api.core.configs import project_settings as settings

def _attach_port_if_needed(base: str, port: str | int | None) -> str:
    """
    Tambahkan :<port> hanya jika base belum punya port.
    Contoh:
      base=http://localhost, port=7860  -> http://localhost:7860
      base=http://localhost:7860, port=7860 -> http://localhost:7860 (tidak dobel)
    """
    base = base.rstrip("/")
    if not port:
        return base
    # hapus scheme lalu cek apakah sudah ada colon setelah host
    try:
        scheme, rest = base.split("://", 1)
    except ValueError:
        # tidak ada scheme (jarang, tapi amankan)
        rest = base
        scheme = "http"

    # kalau rest sudah punya ':<angka>' berarti sudah ada port
    host_has_port = ":" in rest and rest.rsplit(":", 1)[-1].isdigit()
    return f"{base}:{port}" if not host_has_port else base

@lru_cache(maxsize=1)
def get_langflow_webhook_url() -> str:
    """
    Single source of truth untuk URL webhook Langflow.
    """
    base = settings.LANGFW_BASE_URL.rstrip("/")
    base = _attach_port_if_needed(base, settings.LANGFW_PORT)
    flow_id = settings.LANGFW_FLOW_ID or settings.LANGFW_PROJECT_ID
    if not flow_id:
        raise RuntimeError("LANGFW_FLOW_ID / LANGFW_PROJECT_ID haven't di .env")
    return f"{base}/api/v1/webhook/{flow_id}"
