from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI

def mount(app: FastAPI):
    # mount admin Single Page App (static build downloaded from the fiorinoai-webapp repo)
    mount_webapp_spa(app)

    # note html=False because index.html needs to be injected with runtime information
    app.mount("/app", StaticFiles(directory="/platform/"), name="app")


def mount_webapp_spa(app: FastAPI):
    @app.get("/app/", include_in_schema=False)
    @app.get("/app/{page}", include_in_schema=False)
    @app.get("/app/{page}/", include_in_schema=False)
    def get_admin_single_page_app():

        # the webapp static build is created during docker build from this repo:
        # https://github.com/fiorino-ai/fiorinoai-webapp
        # the files live inside the /platform folder (not visible in volume / cat code)
        return FileResponse("/platform/index.html")