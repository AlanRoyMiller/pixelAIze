from fastapi import FastAPI, File, UploadFile, Request, Form
from pathlib import Path
from src.image_pixelizer import ImagePixelizer  # Adjust the import statement based on your project structure
import os
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import tempfile

app = FastAPI()

#create a directory for uploaded images if it doesn't exist

if not os.path.exists("uploaded_images"):
    os.makedirs("uploaded_images/original", exist_ok=True)
    os.makedirs("uploaded_images/pixelated", exist_ok=True)

if not os.path.exists("output"):
    os.makedirs("output/pixelated_images/", exist_ok=True)
    os.makedirs("output/depixelated_images/", exist_ok=True)

app.mount("/output", StaticFiles(directory="output/pixelated_images/"), name="output")
app.mount("/depixelated", StaticFiles(directory="output/depixelated_images/"), name="depixelate")

templates = Jinja2Templates(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")))

@app.get("/")
def read_root():
    return RedirectResponse(url="/upload/")

@app.get("/upload/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("upload_photo.html", {"request": request})


@app.post("/upload/")
async def create_upload_file(file: UploadFile, request: Request):

    file_bytes = await file.read()
    
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(file_bytes)
        temp.flush()  

        pixelizer = ImagePixelizer()
        key = pixelizer.pixelize_image(temp.name, "output/pixelated_images/" + file.filename)
        
    os.unlink(temp.name)

    image_url = f"/output/{file.filename}"

    return templates.TemplateResponse("index.html", {"request": request, "image_url": image_url, "key": key})



@app.get("/depixelate/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("upload_photo copy.html", {"request": request})


@app.post("/depixelate/")
async def create_upload_file(request: Request, file: UploadFile, encryption_key: str = Form(...)):
    # Read the uploaded file in memory
    file_bytes = await file.read()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(file_bytes)
        temp.flush()  # Ensure all data is written to the file before reading it

        # Now you can use temp.name as a file path input to your depixelize_image function
        pixelizer = ImagePixelizer()
        pixelizer.depixelize_image(temp.name, "output/depixelated_images/" + file.filename, encryption_key)
        
    # Delete the temporary file after use
    os.unlink(temp.name)

    image_url = f"/depixelated/{file.filename}"
    return templates.TemplateResponse("index copy.html", {"request": request, "image_url": image_url})


