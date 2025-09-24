from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS add kar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root pe website dikhao
@app.get("/")
async def read_root():
    return FileResponse('templates/index.html')

# Static files serve karo
app.mount("/static", StaticFiles(directory="static"), name="static")

# Tera existing health endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}

# Tera existing predict endpoint (jo bhi hai woh yahan rahega)
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Tera prediction code yahan ayega
    return {"prediction": "result"}