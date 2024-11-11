FROM python:3.11-slim

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY file_client/ /service/file_client/
WORKDIR /service/file_client
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/file_service.proto

EXPOSE 8000
CMD ["uvicorn", "file_client:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]