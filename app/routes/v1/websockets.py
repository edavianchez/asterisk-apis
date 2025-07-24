import json
import asyncio
from typing import Annotated

from fastapi import (
    APIRouter, status as http_status,
    Path, WebSocket, Depends,
    WebSocketDisconnect
)
from fastapi.responses import JSONResponse
from app.dependencies import get_conn_manager
from app.services.connections import ConnectionManager

from app.core.config import settings

logger = settings.logger
ami = settings.asterisk.ami


router = APIRouter(
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {"application/json": {"example": {"detail": "Not Found"}}},
        },
    },
)


@router.websocket("/agents/status/{rrhh_id}")
async def status(
    websocket: WebSocket,
    conn_manager: Annotated[ConnectionManager, Depends(get_conn_manager)],
    rrhh_id: Annotated[str, Path(examples=["12345"])],
):
    """
    WebSocket endpoint to listen for queue status updates.
    """
    await websocket.accept()
    conn_manager.websockets.add_status_table_connections({
        "ws": websocket,
        "rrhh_id": rrhh_id
    })
    try:
        while True:
            msg = await websocket.receive_text()
            msg = json.loads(msg)
            if "queues" in msg:
                data = conn_manager.status_table.get_status(msg["queues"])
                await conn_manager.websockets.send(websocket, data)
            refresh_time = msg["refresh_time"] if "refresh time" in msg else 1

            # Enviar mensaje cada X segundos
            async def send_periodic_message():
                while True:
                    await asyncio.sleep(refresh_time)  # cada x segundos
                    data = conn_manager.status_table.get_status(msg["queues"])
                    await conn_manager.websockets.send(websocket, data)

            # Iniciar la tarea de envío periódico solo una vez
            if not hasattr(websocket, "periodic_task"):
                websocket.periodic_task = asyncio.create_task(
                    send_periodic_message()
                )
    except WebSocketDisconnect:
        conn_manager.websockets.remove_status_table_connections(rrhh_id)
        try:
            websocket.periodic_task.cancel()
        except AttributeError:
            pass
    except (ConnectionError, RuntimeError, asyncio.CancelledError) as e:
        logger.error("Error WebSocket: %s", str(e), exc_info=True)
        conn_manager.websockets.remove_status_table_connections(rrhh_id)
        try:
            await websocket.close()
        except (RuntimeError, WebSocketDisconnect):
            pass


@router.get(
    "/agents/status/info",
    status_code=http_status.HTTP_200_OK,
    summary="Información para conectar el WebSocket de estado de gestión de los agentes"
)
async def status_info():
    """
    Este endpoint proporciona la información necesaria para conectar el WebSocket de estado de gestión de los agentes.\n
    **URL de conexión:** `ws://<dns>/ws/v1/agents/status/:rrhh_id`\n
    **Parámetros de ruta**\n
    - `rrhh_id`: Identificador del cliente que establece la conexión.\n
    **Parámetros de Mensajes**\n
    - `queues_names`: Lista de nombres de colas de las cuales desea recibir información.\n
    - `refresh_time`: (opcional) Tiempo en segundos para obtener los datos actualizados\n
    - **Nota**: Si no se especifica el queues_names, no se recibirán datos.\n
    **Respuesta**\n
    ```json
    [
        {
        "status": "WebSocket is active",
            "queues": ["Q8", "Q5"]
        }
    ]
    ```

    """
    return JSONResponse({
        "url": f"ws://{settings.app_url}/ws/v1/agents/status/:rrhh_id",
        "body_example": {
            "queues_names": ["Q8", "Q5"],
            "refresh_time": 10
        },
        "response_example": [
            {
                "status": "WebSocket is active",
                "queues": ["Q8", "Q5"]
            }
        ]
    })


@router.websocket("/queued/calls/count/{rrhh_id}")
async def queued_calls_count(
    websocket: WebSocket,
    conn_manager: Annotated[ConnectionManager, Depends(get_conn_manager)],
    rrhh_id: Annotated[str, Path(examples=["12345"])],
):
    """
    WebSocket endpoint to listen for queued calls count updates.
    """
    await websocket.accept()
    conn_manager.websockets.add_count_queued_calls_connections({
        "ws": websocket,
        "rrhh_id": rrhh_id,
    })
    try:
        while True:
            msg = await websocket.receive_text()
            msg = json.loads(msg)
            if "queues" in msg:
                data = conn_manager.status_table.get_queued_calls(
                    msg["queues"]
                )
                await conn_manager.websockets.send(websocket, {
                    "count": data["count_queued_calls"]
                })
            refresh_time = msg["refresh_time"] if "refresh time" in msg else 1

            # Enviar mensaje cada X segundos
            async def send_periodic_message():
                while True:
                    await asyncio.sleep(refresh_time)  # cada x segundos
                    data = conn_manager.status_table.get_queued_calls(
                        msg["queues"]
                    )
                    await conn_manager.websockets.send(websocket, {
                        "count": data["count_queued_calls"]
                    })

            # Iniciar la tarea de envío periódico solo una vez
            if not hasattr(websocket, "periodic_task"):
                websocket.periodic_task = asyncio.create_task(
                    send_periodic_message()
                )
    except WebSocketDisconnect:
        conn_manager.websockets.remove_count_queued_calls_connections(rrhh_id)
        try:
            websocket.periodic_task.cancel()
        except AttributeError:
            pass
    except (ConnectionError, RuntimeError, asyncio.CancelledError) as e:
        logger.error("Error WebSocket: %s", str(e), exc_info=True)
        conn_manager.websockets.remove_status_table_connections(rrhh_id)
        try:
            await websocket.close()
        except (RuntimeError, WebSocketDisconnect):
            pass
