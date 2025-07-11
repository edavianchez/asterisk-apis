import asyncio
from fastapi import APIRouter, status as http_status, Path, Body
from fastapi.responses import JSONResponse
from typing import Annotated, List
from panoramisk import Manager

from app.services.queues import Queues
from app.schemas.responses.queue import Queue
from app.schemas.responses.queue_member import QueueMember
from app.dependencies import AMIManager
from app.core.exceptions import (
    NoQueuesFoundException,
    QueueNotFoundException,
    MemberNotFoundException,
)


router = APIRouter(
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        },
    },
)


@router.get("/", status_code=http_status.HTTP_200_OK, response_model=List[Queue])
async def list(manager: Annotated[Manager, AMIManager]):
    """
    List all queues.
    """
    response = await manager.send_action({'Action': 'QueueStatus'})
    queues_info = Queues.map(response)
    if not queues_info:
        raise NoQueuesFoundException()
    return queues_info


@router.get("/{queue_name}", status_code=http_status.HTTP_200_OK, response_model=Queue)
async def show(queue_name: Annotated[str, Path(examples=["Q5"])], manager: Annotated[Manager, AMIManager]):
    """ Show details of a specific queue."""
    action = {'Action': 'QueueStatus', 'Queue': queue_name}
    response = await manager.send_action(action)
    queue_info = Queues.map_details(response, queue_name)
    if not queue_info:
        raise QueueNotFoundException(queue_name)
    return queue_info


# @router.get("/{queue_name}/members", status_code=http_status.HTTP_200_OK, response_model=List[QueueMember])
async def members(queue_name: Annotated[str, Path(examples=["Q5"])], manager: Annotated[Manager, AMIManager]):
    """
    List all members of a specific queue.
    """
    action = {'Action': 'QueueStatus', 'Queue': queue_name}
    response = await manager.send_action(action)
    members_info = Queues.map_members(response, queue_name)
    if not members_info:
        raise MemberNotFoundException(queue_name)
    return members_info


@router.post("/in", status_code=http_status.HTTP_200_OK, response_model=List[Queue])
async def in_queues(
    queues_names: Annotated[List[str], Body(examples=[["Q8", "Q5"]])],
    manager: Annotated[Manager, AMIManager]
):
    """
    List all queues that have members.
    """
    tasks = [manager.send_action(
        {'Action': 'QueueStatus', 'Queue': queue_name}) for queue_name in queues_names]
    responses = await asyncio.gather(*tasks)

    queues_info = []
    for response in responses:
        queue_info = Queues.map(response)
        if queue_info:
            queues_info.append(queue_info[0])

    if not queues_info:
        raise NoQueuesFoundException()
    return queues_info


# @router.post("/add/member", status_code=http_status.HTTP_200_OK)
async def add_member(
    queues_names: Annotated[List[str], Body(examples=["Q5", "Q8"])],
    member_name: Annotated[str, Body(examples=["1001"])],
    manager: Annotated[Manager, AMIManager]
):
    """
    Add a member to a specific queues.
    """
    tasks = [
        manager.send_action({
            'Action': 'QueueAdd',
            'Queue': queue_name,
            'Interface': f'SIP/{member_name}'
        }) for queue_name in queues_names
    ]
    responses = await asyncio.gather(*tasks)

    results = {"success": [], "failed": []}
    for i, response in enumerate(responses):
        queue_name = queues_names[i]
        if response.get('Response') == 'Success':
            results["success"].append(queue_name)
        else:
            error_message = response.get('Message', 'Unknown error')
            results["failed"].append(
                {"queue": queue_name, "error": error_message})

    if not results["success"]:
        return JSONResponse(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            content={
                "message": f"Failed to add member {member_name} to any queue",
                "details": results["failed"]
            }
        )

    if results["failed"]:
        return JSONResponse(
            status_code=http_status.HTTP_207_MULTI_STATUS,
            content={
                "message": f"Partially added member {member_name} to queues",
                "added_to": results["success"],
                "failed_for": results["failed"]
            }
        )

    return {
        "message": f"Successfully added member {member_name} to all queues",
        "queues": results["success"]
    }
