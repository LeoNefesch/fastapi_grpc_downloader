FROM python:3.11-slim

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY file_server/ /service/file_server/
WORKDIR /service/file_server
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/file_service.proto

EXPOSE 50051
ENTRYPOINT [ "python", "file_server.py" ]