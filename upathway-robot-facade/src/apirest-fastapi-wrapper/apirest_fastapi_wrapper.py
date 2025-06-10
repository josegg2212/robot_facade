import json
import sys
import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class ApiRestWrapper:

    """
    routes: [(url, methods, callback)]
    """
    def __init__(self,host="0.0.0.0",port="8080",endpoint="/swagger",title="FastAPI",description="FastAPI description",version="0.0.0"):
        self.title=title
        self.description=description
        self.endpoint=endpoint
        self.version=str(version)
        self.host=host
        self.port=int(port)
        self.endpoint_json=self.endpoint+".json"

        self.app = FastAPI(
            title=self.title,
            description=self.description,
            version=self.version,
            openapi_url=self.endpoint_json,
            docs_url=self.endpoint
        )

    def setup_routes(self, routes):
        for url, methods, callback, tags in routes:
            self.app.add_api_route(url, callback, methods=methods, tags=[tags])

    def run_app(self):
        uvicorn.run(self.app, host=self.host, port=self.port)


if __name__ == "__main__":
    api=ApiRestWrapper("0.0.0.0","8086","/drupal-manager","Drupal Manager","Interfaz de interacción con drupal","0.0.0")
  
    api.setup_routes([
    ("/hello", ["GET"], lambda: {"message": "Hello World"}, "Genéricas"),
    ("/status", ["GET"], lambda: {"status": "OK"}, "Específicas")
    ])
    
    api.run_app()