from fastapi import FastAPI, File, UploadFile, Request, Form
from pathlib import Path
from src.image_pixelizer import ImagePixelizer  # Adjust the import statement based on your project structure
import os
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#create a directory for uploaded images if it doesn't exist

if not os.path.exists("uploaded_images/pixelated_images/"):
    os.makedirs("uploaded_images/pixelated_images/")
if not os.path.exists("output/pixelated_images/"):
    os.makedirs("output/pixelated_images/")

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
    key = pixelizer.pixelize_image(input_path, output_path)

    image_url = f"/output/{file.filename}"

    return templates.TemplateResponse("index.html", {"request": request, "image_url": image_url, "key": key})



@app.get("/depixelate/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("upload_photo copy.html", {"request": request})


@app.post("/depixelate/")
async def create_upload_file(request: Request, file: UploadFile, encryption_key: str = Form(...)):
    print(f"Received key: {encryption_key}")
    input_path = Path("uploaded_images") / file.filename
    output_path = Path("output/depixelated_images") / file.filename

    with open(input_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Create an instance of ImagePixelizer and process the image
    pixelizer = ImagePixelizer()
    pixelizer.depixelize_image(input_path, output_path, encryption_key)

    image_url = f"/output/{file.filename}"
    return templates.TemplateResponse("upload_photo copy.html", {"request": request, "image_url": output_path})

