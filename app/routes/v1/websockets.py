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
            print(msg)
            msg = json.loads(msg)
            if "queues" in msg:
                await conn_manager.add_queues_to_send(rrhh_id, msg["queues"])
            logger.info(f"Msg from client: {msg}")

            # Enviar mensaje cada X segundos
            async def send_periodic_message():
                while True:
                    await asyncio.sleep(10)  # cada 10 segundos
                    await websocket.send_text(json.dumps({"message": "Mensaje periódico"}))
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
        conn_manager.remove_websocket(websocket, rrhh_id)
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
    **URL de conexión:** `ws://<dns>/ws/v1/agents/status/{rrhh_id}`\n
    **Parametros de ruta**\n
    - `rrhh_id`: Identificador del cliente que establece la conexión.\n
    **Cuerpo de la petición (opcional)**\n
    - `queues_names`: Lista de nombres de colas de las cuales desea recibir información.\n
    - **Ejemplo**: `["Q8", "Q5"]`\n
    - **Nota**: Si no se especifica, se recibirán actualizaciones de todas las colas.\n
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
        "url": f"ws://{settings.app_url}/ws/v1/agents/status/20",
        "body_example": {
            "queues_names": ["Q8", "Q5"]
        },
        "response_example": [
            {
                "status": "WebSocket is active",
                "queues": ["Q8", "Q5"]
            }
        ]
    })
