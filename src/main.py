import sys 
from pathlib import Path

from fastapi.responses import JSONResponse
sys.path.append(str(Path(__file__).resolve().parent))
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import Response

app = FastAPI()

@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": request.headers.get("access-control-request-headers", "*"),
            "Access-Control-Allow-Credentials": "true",
        },
    )

# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={"message": str(exc)},
#     )

#Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
                "https://localhost",
                "http://localhost",
                "capacitor://localhost",
                "ionic://localhost",  
                "https://milliary-polyphyletically-hertha.ngrok-free.dev"      
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Section imports
from CONTROLLER.authorizationController import authRoute
from CONTROLLER.wineController import wineRoute

# Incluye las rutas definidas en el archivo 'controllers.py'
#Section include

app.include_router(authRoute)
app.include_router(wineRoute)