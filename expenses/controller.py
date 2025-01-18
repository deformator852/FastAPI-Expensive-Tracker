from fastapi import APIRouter, Depends, HTTPException
from database import SessionDep
from expenses.service import ExpensesService
from schemas.expense import CreateExpense, UpdateExpense
from utilities.current_user import get_current_user


router = APIRouter(tags=["Expenses"])
service = ExpensesService()


@router.put("/expenses/{expense_id}")
async def update_expense(
    data_expense: UpdateExpense,
    expense_id: int,
    session: SessionDep,
    current_user: int = Depends(get_current_user),
): ...


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int, session: SessionDep, current_user: int = Depends(get_current_user)
): ...
@router.get("/expenses/{expense_id}")
async def get_detail_expense(
    expense_id: int, session: SessionDep, current_user: int = Depends(get_current_user)
): ...


@router.get("/expenses/by-amount")
async def get_expenses_by_amount(
    session: SessionDep, current_user: int = Depends(get_current_user)
): ...


@router.get("/expenses")
async def get_expenses(
    session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        data = await service.get_expenses(current_user, session)
        return {"status": True, "expenses": data}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(404, f"can't get expenses.{str(e)}")


@router.post("/expenses")
async def create_expense(
    data_expense: CreateExpense,
    session: SessionDep,
    current_user: int = Depends(get_current_user),
):
    try:
        data = data_expense.model_dump()
        await service.create_expense(data, current_user, session)
        return {"status": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(404, f"can't create this expense.{str(e)}")
