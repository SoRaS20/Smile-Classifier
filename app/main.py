from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
import shutil
import os
from datetime import datetime
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import cv2
import mysql.connector
# from database import Base,engine

# Load the trained model
with open('smile_classifier.pkl', 'rb') as f:
    model = pickle.load(f)

# Base.metadata.create_all(bind=engine)

# Initialize FastAPI and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/uploaded_images", StaticFiles(directory="uploaded_images"), name="uploaded_images")

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="mysql_container",
        user="root",
        password="787898",
        database="smile_classifier"
    )


# Function to create the history table if it doesn't exist
def create_history_table():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Define the SQL statement to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_path VARCHAR(255) NOT NULL,
            label INT NOT NULL,
            datetime DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Execute the query to create the table
        cursor.execute(create_table_query)
        db.commit()
        db.close()
        print("Table 'history' created successfully or already exists.")
    except Exception as e:
        print(f"Error creating table: {str(e)}")


# Call the function on app startup
@app.on_event("startup")
async def startup_event():
    create_history_table()

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/classify", response_class=HTMLResponse)
async def classify(request: Request, message: str = None):
    return templates.TemplateResponse("classify.html", {"request": request, "message": message})



class ImageUploadRequest(BaseModel):
    image: UploadFile


from fastapi import HTTPException
from fastapi.responses import RedirectResponse

@app.post("/classify")
async def upload_image(request: Request, file: UploadFile = File(...)):
    try:
        # Ensure the uploaded file is an image
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Save the uploaded file
        if not os.path.exists("uploaded_images"):
            os.makedirs("uploaded_images")
        image_path = f"uploaded_images/{file.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Preprocess the image
        img = cv2.imread(image_path)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid or corrupted image file")
        img_resized = cv2.resize(img, (64, 64))
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY).flatten()

        # Predict using the model (model might expect a 2D array for single image)
        prediction = model.predict(img_gray.reshape(1, -1))

        # Convert NumPy data type to a native Python type
        predicted_label = 1 if prediction[0] > 0.5 else 0  # For binary classification

        print(f"Prediction: {prediction}")
        print(f"prediction level: {predicted_label}")
        label = "smiling" if predicted_label == 1 else "not smiling"
        # Save the result in the database
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO history (image_path, label, datetime) VALUES (%s, %s, %s)",
            (image_path, predicted_label, datetime.now())
        )
        db.commit()
        db.close()

        # Redirect to the classify page with a success message
        return RedirectResponse(url="/classify?message=inserted_successfully", status_code=303)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# History page
@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM history")
    result = cursor.fetchall()
    db.close()

    return templates.TemplateResponse("history.html", {"request": request, "history": result})

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)














