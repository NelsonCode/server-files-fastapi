from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove
from shutil import rmtree

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(getcwd() + "/" + file.filename, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    return "success"


@router.get("/file/{name_file}")
def get_file(name_file: str):
    return FileResponse(getcwd() + "/" + name_file)


@router.get("/download/{name_file}")
def download_file(name_file: str):
    return FileResponse(getcwd() + "/" + name_file, media_type="application/octet-stream", filename=name_file)


@router.delete("/delete/{name_file}")
def delete_file(name_file: str):
    try:
        remove(getcwd() + "/" + name_file)
        return JSONResponse(content={
            "removed": True
        }, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "message": "File not found"
        }, status_code=404)


@router.delete("/folder")
def delete_file(folder_name: str = Form(...)):
    rmtree(getcwd() + folder_name)
    return JSONResponse(content={
        "removed": True
    }, status_code=200)
