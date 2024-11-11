import os
from typing import AsyncGenerator
from urllib.parse import quote

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import grpc

import file_service_pb2 as pb2
import file_service_pb2_grpc as pb2_grpc


app = FastAPI()
file_server_host = os.getenv("FILE_SERVER_HOST", "localhost")
channel = grpc.aio.insecure_channel(f"{file_server_host}:50051")
client_side = pb2_grpc.FileServiceStub(channel)
ONE_MB = 1024 * 1024


async def file_upload_generator(
        filename: str,
        file: UploadFile) -> AsyncGenerator[pb2.UploadFileRequest, None]:
    yield pb2.UploadFileRequest(filename=filename, content=b"")
    while chunk := await file.read(ONE_MB):
        yield pb2.UploadFileRequest(content=chunk)


@app.post("/upload-file/")
async def upload_file(filename: str, file: UploadFile):
    response = await client_side.UploadFile(file_upload_generator(filename, file))
    return {"message": response.message}


@app.get("/get-file/")
async def get_file(filename: str):
    request = pb2.GetFileRequest(filename=filename)
    utf8_filename = quote(filename)

    async def file_stream() -> AsyncGenerator[bytes, None]:
        try:
            async for response in client_side.GetFile(request):
                yield response.content
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise HTTPException(status_code=404, detail="File not found")
            raise HTTPException(status_code=500,
                                detail=f"Error: {e.details()}")
    return StreamingResponse(
        file_stream(), media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={utf8_filename}"})
