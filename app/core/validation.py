import logging
from starlette import status
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

logger = logging.getLogger("app.main")

async def Validation_Exeptions_Handler(res:Request,msg:RequestValidationError):
    logger.error(f"validation error:{msg.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "message_error":msg.errors()
        }
    )