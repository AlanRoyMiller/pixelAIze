from fastapi import FastAPI, File, UploadFile, Request
from pathlib import Path
from src.image_pixelizer import ImagePixelizer  # Adjust the import statement based on your project structure
import os
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/output", StaticFiles(directory="output/pixelated_images/"), name="output")
templates = Jinja2Templates(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")))

@app.get("/")
def read_root():
    return RedirectResponse(url="/upload/")

@app.get("/upload/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("upload_photo.html", {"request": request})


@app.post("/upload/")
async def create_upload_file(file: UploadFile, request: Request):
    input_path = Path("uploaded_images") / file.filename
    output_path = Path("output/pixelated_images") / file.filename
    
    # Save the uploaded file to the "uploaded_images" directory
    with open(input_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # Create an instance of ImagePixelizer and process the image
    pixelizer = ImagePixelizer()
    pixelizer.pixelize_image(input_path, output_path)

    image_url = f"/output/{file.filename}"
    return templates.TemplateResponse("index.html", {"request": request, "image_url": image_url})

@app.get("/view/{filename}", response_class=HTMLResponse)
async def view_output(request: Request, filename: str):
    image_url = f"/output/{filename}"
    return templates.TemplateResponse("index.html", {"request": request, "image_url": image_url})
