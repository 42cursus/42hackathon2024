import shutil
from typing_extensions import Annotated
from fastapi import (
    APIRouter, Request, File, UploadFile
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router = APIRouter()
templates = Jinja2Templates(directory="../templates/")


@router.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(
        file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}


@router.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse(
        "uploadfile.html", {"request": request}
    )


@router.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f'upload/{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}
