from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.deps import get_db
from app.api.deps import get_current_user
from app.schemas.group import GroupCreate
from app.services import group_service
from app.models import GroupTransaction, GroupMember, User, Transaction

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("/")
def create_group(
    data: GroupCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return group_service.create_group_transaction(current_user, data, db)


@router.get("/")
def get_my_groups(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Groups the user created or is a member of."""
    uid = current_user.id

    # Groups I created
    created = db.query(GroupTransaction).filter(
        GroupTransaction.creator_id == uid
    ).all()

    # Groups I'm a member of (not creator)
    member_group_ids = [
        m.group_id for m in
        db.query(GroupMember.group_id).filter(GroupMember.user_id == uid).all()
    ]
    as_member = db.query(GroupTransaction).filter(
        GroupTransaction.id.in_(member_group_ids),
        GroupTransaction.creator_id != uid
    ).all()

    all_groups = {g.id: g for g in created + as_member}

    result = []
    for g in sorted(all_groups.values(), key=lambda x: x.created_at, reverse=True):
        # Get members
        members = (
            db.query(User.id, User.username, GroupMember.share_amount)
            .join(GroupMember, GroupMember.user_id == User.id)
            .filter(GroupMember.group_id == g.id)
            .all()
        )
        # Get related transactions
        txns = db.query(Transaction).filter(
            Transaction.lender_id == g.creator_id,
            Transaction.description.like(f"%[Group #{g.id}]%")
        ).all()

        settled   = sum(1 for t in txns if t.status.value in ("settled", "auto_settled"))
        pending   = sum(1 for t in txns if t.status.value == "pending")
        total_ppl = len(members) + 1  # members + creator

        result.append({
            "id":          g.id,
            "description": g.description or "",
            "total_amount": float(g.total_amount),
            "share":        float(g.total_amount) / total_ppl if total_ppl else 0,
            "created_at":   g.created_at.isoformat(),
            "is_creator":   g.creator_id == uid,
            "member_count": total_ppl,
            "settled_count": settled,
            "pending_count": pending,
            "members": [
                {"id": m.id, "username": m.username,
                 "share": float(m.share_amount)}
                for m in members
            ],
        })

    return result