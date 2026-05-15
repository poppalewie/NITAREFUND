from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import TrustScore, User, Transaction


def get_pair_trust(a_id: int, b_id: int, db: Session):
    return (
        db.query(TrustScore)
        .filter(
            TrustScore.user_a_id == a_id,
            TrustScore.user_b_id == b_id
        )
        .first()
    )


def leaderboard(db: Session, limit: int = 10):
    from sqlalchemy import func, or_
    from app.models import Transaction

    # Count transactions per user (as lender or borrower)
    as_lender = (
        db.query(Transaction.lender_id.label("uid"), func.count().label("cnt"))
        .group_by(Transaction.lender_id)
    )
    as_borrower = (
        db.query(Transaction.borrower_id.label("uid"), func.count().label("cnt"))
        .group_by(Transaction.borrower_id)
    )
    from sqlalchemy import union_all
    combined = union_all(as_lender, as_borrower).subquery()
    tx_totals = (
        db.query(combined.c.uid, func.sum(combined.c.cnt).label("total"))
        .group_by(combined.c.uid)
        .subquery()
    )

    results = (
        db.query(
            User.id,
            User.username,
            func.coalesce(func.avg(TrustScore.score), 50.0).label("avg_score"),
            func.coalesce(tx_totals.c.total, 0).label("tx_count"),
        )
        .outerjoin(TrustScore, TrustScore.user_b_id == User.id)
        .outerjoin(tx_totals, tx_totals.c.uid == User.id)
        .group_by(User.id, User.username, tx_totals.c.total)
        .order_by(func.coalesce(func.avg(TrustScore.score), 50.0).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "user_id":           r.id,
            "username":          r.username,
            "score":             round(float(r.avg_score), 1),
            "transaction_count": int(r.tx_count),
        }
        for r in results
    ]


def get_my_network(user_id: int, db: Session):
    """
    Every peer the user has ever transacted with,
    plus their pairwise trust score (outgoing: how I rated them).
    Falls back to 50 if no score exists yet.
    """
    from sqlalchemy import or_, union, func
    from app.models import Transaction

    # Collect all unique peer IDs from transactions
    as_lender   = db.query(Transaction.borrower_id.label("peer_id")).filter(
        Transaction.lender_id == user_id)
    as_borrower = db.query(Transaction.lender_id.label("peer_id")).filter(
        Transaction.borrower_id == user_id)

    peer_ids = union(as_lender, as_borrower).subquery()

    results = (
        db.query(
            User.id,
            User.username,
            func.coalesce(TrustScore.score, 50.0).label("score")
        )
        .select_from(peer_ids)
        .join(User, User.id == peer_ids.c.peer_id)
        .outerjoin(
            TrustScore,
            (TrustScore.user_a_id == user_id) &
            (TrustScore.user_b_id == User.id)
        )
        .distinct()
        .order_by(func.coalesce(TrustScore.score, 50.0).desc())
        .all()
    )

    return [
        {
            "user_id":  r.id,
            "username": r.username,
            "score":    round(float(r.score), 1),
        }
        for r in results
    ]