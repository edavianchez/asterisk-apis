from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

from app.core.config import settings

logger = settings.logger


class WebSocketManager:
    """Manages WebSocket connections for real-time status table and queued calls monitoring.

    This class handles the lifecycle of WebSocket connections, including:
    - Adding and removing connections for status table updates
    - Adding and removing connections for queued calls count updates
    - Sending data to connected clients
    - Closing all connections when needed
    """

    def __init__(self):
        self.__connections: list[WebSocket] = []
        self.__status_table_connections: list[dict[str, Any]] = []
        self.__count_queued_calls_connections: list[dict[str, Any]] = []

    def add_status_table_connections(self, connection: dict[str, Any]) -> None:
        """Add a new connection to the status table connections list.

        Args:
            connection (dict[str, Any]): Dictionary containing connection details and metadata
        """
        self.__status_table_connections.append(connection)
        self.__connections.append(connection["ws"])
        logger.info(
            "WebSocket añadido a la lista de conexiones de la tabla de estado. Total: %d",
            len(self.__status_table_connections)
        )

    def add_count_queued_calls_connections(self, connection: dict[str, Any]) -> None:
        """Add a new connection to the count queued calls connections list.

        Args:
            connection (dict[str, Any]): Dictionary containing connection details and metadata
        """
        self.__count_queued_calls_connections.append(connection)
        self.__connections.append(connection["ws"])
        logger.info(
            "WebSocket añadido a la lista de conexiones del conteo de llamadas en cola. Total: %d",
            len(self.__count_queued_calls_connections)
        )

    def remove_status_table_connections(self, rrhh_id: str) -> None:
        """Remove a connection from the list of connections by rrhh_id.

        Args:
            rrhh_id (str): The rrhh_id of the connection to remove
        """
        for connection in self.__status_table_connections:
            if connection["rrhh_id"] == rrhh_id:
                self.__status_table_connections.remove(connection)
                self.__connections.remove(connection["ws"])
                logger.info(
                    "WebSocket removido de la lista de conexiones por rrhh_id: %s",
                    rrhh_id
                )
                break

    def remove_count_queued_calls_connections(self, rrhh_id: str) -> None:
        """Remove a connection from the list of connections by rrhh_id.

        Args:
            rrhh_id (str): The rrhh_id of the connection to remove
        """
        for connection in self.__count_queued_calls_connections:
            if connection["rrhh_id"] == rrhh_id:
                self.__count_queued_calls_connections.remove(connection)
                self.__connections.remove(connection["ws"])
                logger.info(
                    "WebSocket removido de la lista de conexiones del conteo de llamadas en cola por rrhh_id: %s",
                    rrhh_id
                )
                break

    async def send(self, ws: WebSocket, data: dict[str, Any]) -> None:
        """Send the status table data to all connections.

        Args:
            data (dict[str, Any]): The data to send
        """
        await ws.send_json(data)

    def close_and_remove_connections(self) -> None:
        """Close all WebSocket connections and remove them from the list."""
        for ws in self.__connections:
            try:
                ws.close()
            except (WebSocketDisconnect, ConnectionError, RuntimeError):
                pass
        self.__connections.clear()
        self.__status_table_connections.clear()
        self.__count_queued_calls_connections.clear()
        logger.info("Todas las conexiones WebSocket cerradas y removidas")
