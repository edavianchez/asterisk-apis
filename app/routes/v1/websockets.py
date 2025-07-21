import json
import asyncio
from fastapi import (
    APIRouter, status as http_status,
    Body, Path, WebSocket, Depends,
    WebSocketDisconnect
)
from fastapi.responses import JSONResponse
from typing import Annotated
from panoramisk import Manager
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
    await conn_manager.add_websocket(websocket, rrhh_id)
    try:
        while True:
            msg = await websocket.receive_text()
            msg = json.loads(msg)
            if "queues" in msg:
                await conn_manager.send({
                    "ws": websocket,
                    "queues": msg["queues"]
                })
            refresh_time = msg["refresh_time"] if "refresh time" in msg else 1

            # Enviar mensaje cada X segundos
            async def send_periodic_message():
                while True:
                    await asyncio.sleep(refresh_time)  # cada x segundos
                    await conn_manager.send({
                        "ws": websocket,
                        "queues": msg["queues"]
                    })

            # Iniciar la tarea de envío periódico solo una vez
            if not hasattr(websocket, "periodic_task"):
                websocket.periodic_task = asyncio.create_task(
                    send_periodic_message()
                )
    except WebSocketDisconnect:
        conn_manager.remove_websocket(rrhh_id)
    except Exception as e:
        logger.error(f"Error WebSocket: {str(e)}")
        conn_manager.remove_websocket(rrhh_id)
        try:
            await websocket.close()
        except Exception:
            pass


@router.get(
    "/agents/status/info",
    status_code=http_status.HTTP_200_OK,
    summary="Informacion para conectar el WebSocket de estado de gestion de los agentes"
)
async def status_info():
    """
    Este endpoint proporciona la información necesaria para conectar el WebSocket de estado de gestion de los agentes.\n
    **URL de conexión:** `ws://<dns>/ws/v1/agents/status/:rrhh_id`\n
    **Parametros de ruta**\n
    - `rrhh_id`: Identificador del cliente que establece la conexión.\n
    **Parametros de Mensajes**\n
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
