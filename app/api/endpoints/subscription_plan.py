from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ... import crud
from .. import deps


router = APIRouter()


@router.post("/create-plan")
def create_plan(
    *,
    db: Session = Depends(deps.get_db),
    subscription_plan_dict: Dict,
) -> Any:
    result = crud.sub_plan.create(db=db, sub_plan_dict=subscription_plan_dict)
    return result


@router.get("/get-plans")
def get_plans(
    db: Session = Depends(deps.get_db)
) -> List:
    subs_plans = crud.sub_plan.get_all_plans(db=db)
    return subs_plans
