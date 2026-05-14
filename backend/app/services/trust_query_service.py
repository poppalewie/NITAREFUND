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


def get_my_network(user_id: int, db: Session):
    """
    Returns users I have trust scores for (A → others)
    """
    results = (
        db.query(TrustScore, User)
        .join(User, User.id == TrustScore.user_b_id)
        .filter(TrustScore.user_a_id == user_id)
        .order_by(TrustScore.score.desc())
        .all()
    )

    return [
        {
            "user_id": user.id,
            "username": user.username,
            "score": float(ts.score)
        }
        for ts, user in results
    ]


def leaderboard(db: Session, limit: int = 10):
    """
    Aggregate incoming trust scores, and count each user's transactions.
    """
    # Subquery: count transactions per user (as lender or borrower)
    tx_count = (
        db.query(
            Transaction.lender_id.label("user_id"),
            func.count().label("cnt")
        )
        .group_by(Transaction.lender_id)
        .union_all(
            db.query(
                Transaction.borrower_id.label("user_id"),
                func.count().label("cnt")
            )
            .group_by(Transaction.borrower_id)
        )
        .subquery()
    )

    tx_totals = (
        db.query(
            tx_count.c.user_id,
            func.sum(tx_count.c.cnt).label("total")
        )
        .group_by(tx_count.c.user_id)
        .subquery()
    )

    results = (
        db.query(
            TrustScore.user_b_id,
            func.avg(TrustScore.score).label("avg_score"),
            User.username,
            func.coalesce(tx_totals.c.total, 0).label("tx_count")
        )
        .join(User, User.id == TrustScore.user_b_id)
        .outerjoin(tx_totals, tx_totals.c.user_id == TrustScore.user_b_id)
        .group_by(TrustScore.user_b_id, User.username, tx_totals.c.total)
        .order_by(func.avg(TrustScore.score).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "user_id":           r.user_b_id,
            "username":          r.username,
            "score":             float(r.avg_score),
            "transaction_count": int(r.tx_count),
        }
        for r in results
    ]