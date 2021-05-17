import time

from fastapi import Request, Response

from app.logger.custom_logger import logger


async def http_logging_middleware(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Running request '{request.method} > {request.url}'")

    response: Response = await call_next(request)

    # request_body = await request.body()
    # request_body = request_body.decode("utf-8")
    # logger.info(f"Request Body: {request_body}")

    process_time = time.time() - start_time
    logger.info(f"Finished running request '{request.method} > {request.url}' in {process_time} seconds")
    logger.info(f"Response Status Code: {response.status_code}")

    return response
