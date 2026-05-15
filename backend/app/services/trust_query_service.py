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
    All users, ordered by their average incoming trust score.
    Users with no scores yet default to 50.
    """
    results = (
        db.query(
            User.id,
            User.username,
            func.coalesce(func.avg(TrustScore.score), 50.0).label("avg_score")
        )
        .outerjoin(TrustScore, TrustScore.user_b_id == User.id)
        .group_by(User.id, User.username)
        .order_by(func.coalesce(func.avg(TrustScore.score), 50.0).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "user_id": r.id,
            "username": r.username,
            "score": float(r.avg_score),
        }
        for r in results
    ]