from fastapi import APIRouter, status as http_status, Depends, Body
from typing import Dict, Annotated
from panoramisk import Manager

from app.services.vicidial import VicidialService
from app.dependencies import AMIManager


router = APIRouter(
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        },
    },
)


@router.post("/execute", status_code=http_status.HTTP_200_OK)
async def execute_command(
    manager: Annotated[Manager, AMIManager],
    body: Dict = Body(
        example={"campaign": 1},
    )
) -> Dict:
    campaign = body.get('campaign')
    operation = body.get('operation')
    service = VicidialService()
    data = await service.execute_command(manager, campaign=campaign, operation=operation)
    return data
