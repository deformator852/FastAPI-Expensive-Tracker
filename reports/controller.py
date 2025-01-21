from fastapi import APIRouter, Depends, HTTPException

from database import SessionDep
from reports.service import ReportsService
from utilities.current_user import get_current_user


router = APIRouter(tags=["Reports"])
service = ReportsService()


@router.get("/reports/category/{cat_id}")
async def get_expenses_by_category(
    cat_id: int, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        expenses_by_category = await service.get_expenses_by_category(
            session, current_user, cat_id
        )
        return {"status": True, "report": expenses_by_category}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")
