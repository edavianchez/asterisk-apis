from fastapi import HTTPException


class AsteriskException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class AsteriskTypeErrorException(AsteriskException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Se presento un error al recibir los datos de Asterisk"
        )
