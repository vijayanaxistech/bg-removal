from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io
import base64

app = FastAPI()

# Allow Shopify frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/remove")
async def remove_background(image_file: UploadFile = File(...)):
    try:
        # Read uploaded file
        file_bytes = await image_file.read()

        # Convert bytes → PIL image
        input_image = Image.open(io.BytesIO(file_bytes))

        # Remove background
        output_image = remove(input_image)

        # Convert output to bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        output_bytes = img_byte_arr.getvalue()

        # Encode to base64 (or upload to storage)
        base64_image = base64.b64encode(output_bytes).decode()

        return {
            "image_base64": f"data:image/png;base64,{base64_image}"
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
