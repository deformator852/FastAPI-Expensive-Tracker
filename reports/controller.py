from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from database import SessionDep
from reports.service import ReportsService
from utilities.current_user import get_current_user


router = APIRouter(tags=["Reports"])
service = ReportsService()


@router.get("/reports/yearly")
async def get_expenses_yearly(
    session: SessionDep,
    current_user: int = Depends(get_current_user),
    csv: bool | None = None,
):
    try:
        report = await service.get_report(session, current_user, weeks=4 * 12)
        answer = {"status": True, "report": report}
        if not csv:
            return answer
        report_in_csv = service.write_report_in_csv(report)
        return StreamingResponse(
            content=report_in_csv,
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="report.csv"'},
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/reports/monthly")
async def get_expenses_monthly(
    session: SessionDep,
    current_user: int = Depends(get_current_user),
    csv: bool | None = None,
):
    try:
        report: list = await service.get_report(session, current_user, weeks=4)
        answer = {"status": True, "report": report}
        if not csv:
            return answer
        else:
            report_in_csv = service.write_report_in_csv(report)
            return StreamingResponse(
                content=report_in_csv,
                media_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="report.csv"'},
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/reports/weekly")
async def get_expenses_weekly(
    session: SessionDep,
    current_user: int = Depends(get_current_user),
    csv: bool | None = None,
):
    try:
        report = await service.get_report(session, current_user, weeks=1)
        answer = {"status": True, "report": report}
        if not csv:
            return answer
        report_in_csv = service.write_report_in_csv(report)
        return StreamingResponse(
            content=report_in_csv,
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment;filename="report.csv"'},
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/reports/category/{cat_id}")
async def get_expenses_by_category(
    cat_id: int,
    session: SessionDep,
    current_user: int = Depends(get_current_user),
    csv: bool | None = None,
):
    try:
        report = [await service.get_report_by_category(session, current_user, cat_id)]
        answer = {"status": True, "report": report}
        if not csv:
            return answer
        report_in_csv = service.write_report_in_csv(report)
        return StreamingResponse(
            content=report_in_csv,
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment;filename="report.csv"'},
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")
