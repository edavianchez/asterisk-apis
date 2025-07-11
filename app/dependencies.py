from fastapi import Request, Depends
from panoramisk import Manager


async def get_ami_manager(request: Request) -> Manager:
    """
    Dependency to get the AMI manager instance from the application state.

    Args:
        request: FastAPI request object

    Returns:
        Manager: Panoramisk AMI manager instance

    Raises:
        RuntimeError: If AMI manager is not available in application state
    """
    manager = getattr(request.app.state, 'manager', None)
    if manager is None:
        raise RuntimeError("AMI manager not available. Check AMI connection.")
    return manager


# Type alias for better code readability
AMIManager = Depends(get_ami_manager)
