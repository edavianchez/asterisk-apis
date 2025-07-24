import asyncio
from panoramisk import Manager

from app.core.config import settings
from app.services.status_table import StatusTable
from app.services.websockets import WebSocketManager

logger = settings.logger
ami = settings.asterisk.ami


class ConnectionManager:
    """Manages AMI (Asterisk Manager Interface) connections and related event handling.

    This class is responsible for:
    - Establishing and maintaining AMI connections
    - Handling Asterisk events (Hold, Unhold, QueueMemberPause, Hangup)
    - Managing the status table updates
    - Coordinating WebSocket connections
    """

    def __init__(self):
        self.ami_manager = None
        self.connection_task = None
        self.status_table = StatusTable()
        self.websockets = WebSocketManager()

    async def start_ami_connection(self):
        """Establishes and maintains the Asterisk Manager Interface (AMI) connection.

        This method:
        - Creates an AMI manager instance with configured credentials
        - Registers event handlers for Hold, Unhold, QueueMemberPause and Hangup events
        - Continuously tries to maintain the connection, reconnecting if needed
        - Loads and periodically reloads the status table data

        The connection loop continues until explicitly cancelled.
        """
        self.ami_manager = Manager(
            host=ami.host,
            port=ami.port,
            username=ami.username,
            secret=ami.password.get_secret_value(),
        )

        async def handle_event(_, event):
            await self.handle_asterisk_event(event)

        self.ami_manager.register_event("Hold", handle_event)
        self.ami_manager.register_event("Unhold", handle_event)
        self.ami_manager.register_event("QueueMemberPause", handle_event)
        self.ami_manager.register_event("Hangup", handle_event)
        # self.ami_manager.register_event("ExtensionStatus", handle_event)
        while True:
            try:
                if not self.ami_manager._connected:
                    logger.info("Conectando a Asterisk AMI...")
                    await self.ami_manager.connect()
                    logger.info("✅ Conexión AMI establecida")
                    await self.status_table.load_data(self.ami_manager)

                await asyncio.sleep(1)
                await self.status_table.reload(self.ami_manager)

            except ConnectionError as e:
                logger.warning(
                    "Error ASCCS1 de conexión AMI: %s. Reconectando...", str(e))
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                logger.info("Conexión AMI cancelada")
                break
            except (OSError, RuntimeError, asyncio.TimeoutError) as e:
                logger.error("Error ASCCS2 crítico en AMI: %s", str(e))
                await asyncio.sleep(10)

    async def handle_asterisk_event(self, event):
        """Handles incoming Asterisk events and updates the status table accordingly.

        This method processes different types of Asterisk events (Hold, Unhold, 
        QueueMemberPause, Hangup) and delegates the appropriate action to the status table.

        Args:
            event: The Asterisk event object containing event type and related data

        Raises:
            ValueError: If event data is invalid
            KeyError: If required event fields are missing
            AttributeError: If event object is malformed
        """
        try:
            match event.event:
                case "Hold":
                    self.status_table.set_hold_time(event)
                case "Unhold":
                    self.status_table.set_unhold(event)
                case "QueueMemberPause":
                    self.status_table.add_pause(event)
                case "Hangup":
                    self.status_table.listen_hangup(event)
                case "ExtensionStatus":
                    logger.info("%s: %s", event.event, event)
        except (ValueError, KeyError, AttributeError) as e:
            logger.error("Error ASCCH1 procesando evento: %s", str(e))

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
                except (ConnectionError, OSError) as e:
                    logger.error(
                        "Error ASCCC1 cerrando conexión AMI: %s", str(e)
                    )
                finally:
                    self.ami_manager = None

            # Cerrar todas las conexiones WebSocket
            self.websockets.close_and_remove_connections()

        except (RuntimeError, OSError) as e:
            logger.error("Error ASCCC2 en cierre: %s", str(e))
