from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI

def mount_platform(app: FastAPI):
    """Mount platform static files and handle SPA routing"""
    
    # Mount static files
    app.mount("/platform", StaticFiles(directory="app/platform", html=True), name="platform")

    @app.get("/", include_in_schema=False)
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_platform(full_path: str = ""):
        # Skip API routes
        if full_path.startswith("api/"):
            return None
            
        # Serve index.html for all other routes (SPA routing)
        return FileResponse("app/platform/index.html") 