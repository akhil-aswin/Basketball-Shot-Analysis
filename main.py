import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers.api import router

app = FastAPI(title='NBA Shot Chart')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router, prefix='/api')

# Serve built React frontend (production)
_dist = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
if os.path.exists(_dist):
    app.mount('/assets', StaticFiles(directory=os.path.join(_dist, 'assets')), name='assets')

    @app.get('/{full_path:path}')
    def serve_spa(full_path: str):
        return FileResponse(os.path.join(_dist, 'index.html'))
