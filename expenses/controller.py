from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from database import SessionDep
from expenses.service import ExpensesService
from schemas.expense import CreateExpense, UpdateExpense
from utilities.current_user import get_current_user


router = APIRouter(tags=["Expenses"])
service = ExpensesService()


@router.get("/expenses/by-max-amount/{amount}")
async def get_expenses_by_max_amount(
    amount: float, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        expenses = await service.get_expenses_by_amount(
            current_user, session, max_amount=amount
        )
        return {"status": True, "expenses": expenses}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/expenses/by-min-amount/{amount}")
async def get_expenses_by_min_amount(
    amount: float, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        expenses = await service.get_expenses_by_amount(
            current_user, session, min_amount=amount
        )
        return {"status": True, "expenses": expenses}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/expenses/by-category/{cat_id}")
async def get_expenses_by_category(
    cat_id: int, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        expenses = await service.get_expenses_by_category(current_user, cat_id, session)
        return {"status": True, "expenses": expenses}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/expenses/{expense_id}")
async def get_detail_expense(
    expense_id: int, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        expense = await service.get_expense_by_id(current_user, expense_id, session)
        return {"status": True, "expense": expense}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        await service.delete_expense(current_user, expense_id, session)
        return {"status": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.patch("/expenses/{expense_id}")
async def update_expense(
    data_expense: UpdateExpense,
    expense_id: int,
    session: SessionDep,
    current_user: int = Depends(get_current_user),
):
    data = data_expense.model_dump(exclude_none=True)
    try:
        await service.update_expense(current_user, expense_id, data, session)
        return {"status": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/expenses/by-date-to/{date}")
async def get_expenses_by_date_to(
    date: datetime, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        expenses = await service.get_expenses_by_date(
            current_user, session, date_to=date
        )
        return {"status": True, "expenses": expenses}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/expenses/by-date-from/{date}")
async def get_expenses_by_date_from(
    date: datetime, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        expenses = await service.get_expenses_by_date(
            current_user, session, date_from=date
        )
        return {"status": True, "expenses": expenses}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


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
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


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
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")
