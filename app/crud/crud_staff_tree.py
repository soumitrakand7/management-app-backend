from typing import Dict
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import StaffTree
from app import crud


class CRUDStaffTree(CRUDBase):
    def create(self, db: Session, first_staff_id: str, second_staff_id: str, relation_tag: str, subscriber_group_id: str):
        staff_id = ""
        senior_staff_id = ""
        if relation_tag == "Manager":
            senior_staff_id = second_staff_id
            staff_id = first_staff_id
        else:
            senior_staff_id = first_staff_id
            staff_id = second_staff_id
        db_obj = StaffTree(
            staff_id=staff_id,
            senior_staff_id=senior_staff_id,
            relation_tag=relation_tag,
            subscriber_group_id=subscriber_group_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_staff_tree(self, db: Session, subscriber_group_id: str):
        staff_tree_relations = db.query(StaffTree).filter(
            StaffTree.subscriber_group_id == subscriber_group_id).all()
        staff_member_ids = set()
        for member in staff_tree_relations:
            staff_member_ids.add(member.staff_id)
            staff_member_ids.add(member.senior_staff_id)
        staff_member_ids.discard(None)
        users_list = []
        for id in staff_member_ids:
            staff_obj = crud.staff_management.get_by_id(
                db=db, staff_member_id=id)
            users_list.append(staff_obj.user)
        return {"staff_relations": staff_tree_relations, "users": users_list}


staff_tree = CRUDStaffTree()
