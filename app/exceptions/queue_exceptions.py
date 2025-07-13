from fastapi import HTTPException


class QueueException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class QueueNotFoundException(QueueException):
    def __init__(self, queue_name: str):
        super().__init__(
            status_code=404,
            detail=f"Queue '{queue_name}' not found"
        )


class NoQueuesFoundException(QueueException):
    def __init__(self):
        super().__init__(status_code=404, detail="No queues found")


class MemberNotFoundException(QueueException):
    def __init__(self, queue_name: str):
        super().__init__(
            status_code=404,
            detail=f"No members found for queue '{queue_name}'"
        )
