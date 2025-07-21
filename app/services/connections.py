import asyncio
import json
from typing import Any
from fastapi import WebSocket
from panoramisk import Manager

from app.core.config import settings
from app.services.status_table import StatusTable

logger = settings.logger
ami = settings.asterisk.ami


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[dict[str, Any]] = []
        self.ami_manager = None
        self.connection_task = None
        self.__status_table = StatusTable()

    async def add_websocket(self, websocket: WebSocket, rrhh_id: int):
        self.active_connections.append({
            "ws": websocket,
            "rrhh_id": rrhh_id,
            "queues": []
        })
        logger.info(
            f"WebSocket añadido. Total: {len(self.active_connections)}"
        )

    def remove_websocket(self, rrhh_id: int):
        for ws_item in self.active_connections:
            if ws_item[rrhh_id] == rrhh_id:
                self.active_connections.remove(ws_item)
                break
        logger.info(
            f"WebSocket removido. Total: {len(self.active_connections)}"
        )

    async def send(self, ws: dict[str, Any]):
        data_filtered = self.__status_table.filter(ws["queues"])
        call_filtered = self.__status_table.call_filter(ws["queues"])
        data = {
            "data_table": data_filtered,
            "total_rows": len(data_filtered),
            "counts": self.__status_table.count_by_state(data_filtered),
            "queued_calls": call_filtered,
            "count_queued_calls": len(call_filtered)
        }
        await ws["ws"].send_json(data)

    # async def add_queues_to_send(self, rrhh_id: int, queues: list[str]):
    #     for ws in self.active_connections:
    #         if ws["rrhh_id"] == rrhh_id:
    #             ws["queues"] = queues
    #             if ws["queues"]:
    #                 await self.send(ws)

    # async def broadcast(self):
    #     for ws in self.active_connections:
    #         try:
    #             if ws["queues"]:
    #                 logger.info("Enviando mensaje ...")
    #                 await self.send(ws)
    #                 logger.info("Mensaje enviado.")
    #         except Exception as e:
    #             logger.error(f"Error ASCCB56 enviando mensaje: {str(e)}")
    #             self.remove_websocket(ws)

    async def start_ami_connection(self):
        self.ami_manager = Manager(
            host=ami.host,
            port=ami.port,
            username=ami.username,
            secret=ami.password.get_secret_value(),
        )

        async def handle_event(_, event):
            await self.handle_asterisk_event(event)

        self.ami_manager.register_event("*", handle_event)
        while True:
            try:
                if not self.ami_manager._connected:
                    logger.info("Conectando a Asterisk AMI...")
                    await self.ami_manager.connect()
                    logger.info("✅ Conexión AMI establecida")
                    await self.__status_table.load_data(self.ami_manager)

                await asyncio.sleep(5)
                await self.__status_table.reload(self.ami_manager)

            except ConnectionError as e:
                logger.warning(
                    f"Error ASCCS89 de conexión AMI: {str(e)}. Reconectando...")
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                logger.info("Conexión AMI cancelada")
                break
            except Exception as e:
                logger.error(f"Error ASCCS95 crítico en AMI: {str(e)}")
                await asyncio.sleep(10)

    async def handle_asterisk_event(self, event):
        try:
            event_name = event.event
            # logger.info(f"Llego el evento {event_name}: {event}")
        except Exception as e:
            logger.error(f"Error ASCCH104 procesando evento: {str(e)}")

    async def start(self):
        """Inicia la conexión AMI en segundo plano"""
        if self.connection_task is None or self.connection_task.done():
            self.connection_task = asyncio.create_task(
                self.start_ami_connection()
            )

    async def close(self):
        """Cerrar conexiones al apagar"""
        try:
            # Cancelar la tarea de conexión si existe
            if self.connection_task and not self.connection_task.done():
                self.connection_task.cancel()
                try:
                    await self.connection_task
                except asyncio.CancelledError:
                    pass

            # Cerrar conexión AMI si existe
            if self.ami_manager is not None:
                try:
                    if self.ami_manager._connected:
                        self.ami_manager.close()
                        logger.info("Conexión AMI cerrada")
                except Exception as e:
                    logger.error(
                        f"Error ASCCC131 cerrando conexión AMI: {str(e)}")
                finally:
                    self.ami_manager = None

            # Cerrar todas las conexiones WebSocket
            for ws in list(self.active_connections):
                try:
                    await ws.close()
                except Exception:
                    pass
                self.remove_websocket(ws)

            logger.info("Todas las conexiones cerradas")

        except Exception as e:
            logger.error(f"Error ASCCC146 en cierre: {str(e)}")
