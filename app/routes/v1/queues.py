from fastapi import APIRouter, status as http_status, HTTPException, Request, Path, Body
from fastapi.responses import JSONResponse
from typing import Annotated, List

from app.services.queues import Queues
from app.schemas.responses.queue import Queue
from app.schemas.responses.queue_member import QueueMember


router = APIRouter(
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        },
    },
)


@router.get("/", status_code=http_status.HTTP_200_OK, response_model=List[Queue])
async def list(request: Request):
    """
    List all queues.
    """
    manager = request.app.state.manager
    response = await manager.send_action({'Action': 'QueueStatus'})
    queues_info = Queues.map(response)
    if not queues_info:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="No queues found"
        )
    return queues_info


@router.get("/{queue_name}", status_code=http_status.HTTP_200_OK, response_model=Queue)
async def show(request: Request, queue_name: Annotated[str, Path(example="Q5")]):
    manager = request.app.state.manager
    action = {'Action': 'QueueStatus', 'Queue': queue_name}
    response = await manager.send_action(action)
    queues_info = Queues.map(response)
    if not queues_info:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Queue '{queue_name}' not found"
        )
    return queues_info[0]


@router.get("/{queue_name}/members", status_code=http_status.HTTP_200_OK, response_model=List[QueueMember])
async def members(request: Request, queue_name: Annotated[str, Path(example="Q5")]):
    """
    List all members of a specific queue.
    """
    manager = request.app.state.manager
    action = {'Action': 'QueueStatus', 'Queue': queue_name}
    response = await manager.send_action(action)
    members_info = Queues.map_members(response, queue_name)
    if not members_info:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"No members found for queue '{queue_name}'"
        )
    return members_info


@router.post("/in", status_code=http_status.HTTP_200_OK, response_model=List[Queue])
async def in_queues(request: Request, queues_names: Annotated[List[str], Body(example=["Q8", "Q5"])]):
    """
    List all queues that have members.
    """
    queues_info = []
    manager = request.app.state.manager
    for queue_name in queues_names:
        action = {'Action': 'QueueStatus', 'Queue': queue_name}
        response = await manager.send_action(action)
        queue_info = Queues.map(response)
        if queue_info:
            queues_info.append(queue_info[0])

    if not queues_info:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="No queues with members found"
        )
    return queues_info


@router.post("/add/member", status_code=http_status.HTTP_200_OK)
async def add_member(
    request: Request,
    queues_names: Annotated[List[str], Body(example=["Q5", "Q8"])],
    member_name: Annotated[str, Body(example="1001")],
):
    """
    Add a member to a specific queues.
    """
    errors = []
    manager = request.app.state.manager
    for queue_name in queues_names:
        action = {
            'Action': 'QueueAdd',
            'Queue': queue_name,
            'Interface': f'SIP/{member_name}'
        }
        response = await manager.send_action(action)
        if response.get('Response') != 'Success':
            errors.append(
                f"Failed to add member '{member_name}' to queue '{queue_name}': {response.get('Message', 'Unknown error')}")
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "message": "Member added to queues",
            "errors": errors
        }
    )
