import asyncio
import os

import aiofiles
import grpc

import file_service_pb2 as pb2
import file_service_pb2_grpc as pb2_grpc


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_STORAGE = os.path.join(BASE_DIR, 'file_storage')
ONE_MB = 1024 * 1024


class FileService(pb2_grpc.FileServiceServicer):
    def __init__(self, storage_dir=FILE_STORAGE):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    async def save_chunk_to_file(self, filepath, chunk):
        async with aiofiles.open(filepath, 'ab') as f:
            await f.write(chunk)

    async def UploadFile(self, request_iterator, context):
        filename = None
        filepath = None
        async for request in request_iterator:
            if not filename:
                filename = request.filename
                filepath = os.path.join(self.storage_dir, filename)
            await self.save_chunk_to_file(filepath, request.content)
        return pb2.UploadFileResponse(
            message=f"File '{filename}' uploaded successfully")

    async def GetFile(self, request, context):
        filepath = os.path.join(self.storage_dir, request.filename)
        if not os.path.exists(filepath):
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")
        async with aiofiles.open(filepath, 'rb') as f:
            while chunk := await f.read(ONE_MB):
                yield pb2.GetFileResponse(content=chunk, is_last_chunk=False)
        yield pb2.GetFileResponse(content=b'', is_last_chunk=True)


async def serve():
    server = grpc.aio.server()
    pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
