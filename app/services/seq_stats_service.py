from sqlalchemy.orm import Session
from app.models.device_stats import DeviceStats

def update_seq_stats(db: Session, device_id: int, seq: int):

    stats = db.query(DeviceStats).filter(
        DeviceStats.device_id == device_id
    ).first()

    if not stats:
        stats = DeviceStats(device_id=device_id, last_seq=seq, total_packets=1)
        db.add(stats)
        return

    # detect duplicate
    if seq <= stats.last_seq:
        stats.duplicate_packets += 1
    else:
        missing = seq - stats.last_seq - 1
        if missing > 0:
            stats.missing_packets += missing

        stats.last_seq = seq

    stats.total_packets += 1