# app/services/seq_monitor.py

DEVICE_SEQ_STATE = {}

def check_seq(device_id: int, seq: int | None):
    """
    Detect missing sequence numbers
    """
    if seq is None:
        return {
            "missing": 0,
            "duplicate": False
        }

    state = DEVICE_SEQ_STATE.setdefault(device_id, {
        "last_seq": None,
        "total": 0,
        "missing": 0,
        "duplicate": 0
    })

    last_seq = state["last_seq"]

    missing = 0
    duplicate = False

    if last_seq is not None:

        # 📉 missing samples
        if seq > last_seq + 1:
            missing = seq - last_seq - 1
            state["missing"] += missing

        # 🔁 duplicate or resend
        if seq <= last_seq:
            duplicate = True
            state["duplicate"] += 1

    state["last_seq"] = seq
    state["total"] += 1

    return {
        "missing": missing,
        "duplicate": duplicate
    }


def get_seq_stats(device_id: int):
    state = DEVICE_SEQ_STATE.get(device_id)

    if not state:
        return {
            "total": 0,
            "missing": 0,
            "duplicate": 0,
            "loss_rate": 0
        }

    total = state["total"]
    missing = state["missing"]

    loss_rate = 0
    if total > 0:
        loss_rate = missing / total

    return {
        "total": total,
        "missing": missing,
        "duplicate": state["duplicate"],
        "loss_rate": loss_rate
    }