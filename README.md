# Smile Classifier Web Application

This project is a **FastAPI-based web application** to classify uploaded images as either **smiling** or **not smiling** using a pre-trained Machine Learning model. It also supports storing classification history in a **MySQL database** and displaying it in the app.

---

## Features

- **Upload and Classify Images:** Upload images to classify them into "smiling" or "not smiling" using the **FastAPI backend** and a **trained machine learning model**.
- **Image Preprocessing:** Images are resized, converted to grayscale, and flattened before feeding into the classifier.
- **Database Integration:** Stores classification history (image path, label, timestamp) in a MySQL database.
- **Responsive User Interface:** A web interface designed with **Jinja2 templates** for easy interaction.
- **Dockerized Application:** Fully containerized using **Docker**, with separate containers for the FastAPI app and MySQL database.

---

## Technology Stack

- **Backend Framework:** FastAPI
- **Frontend:** Jinja2 Templates
- **Database:** MySQL
- **Machine Learning Model:** Pre-trained `smile_classifier.pkl` file (Pickle format)
- **Containerization:** Docker and Docker Compose
- **Task Automation:** Using scripts and FastAPI startup events

---

## Prerequisites

Make sure you have the following installed on your machine:
- **Docker** and **Docker Compose**
- **Python 3.10 or above** (if running locally rather than through Docker)
- Libraries listed in `requirements.txt`

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Run Using Docker Compose
Build and start the project containers:
```bash
docker-compose up --build
```
This will:
1. Create a MySQL database container.
2. Launch the FastAPI application, which waits for the database container to start.

The application will be accessible at [http://localhost:8000](http://localhost:8000).

### 3. Run Locally (Without Docker)
If you prefer running the project locally:
1. Install **Python 3.10**.
2. Set up a virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate   # For Linux/macOS
   venv\Scripts\activate      # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Edit `SQLALCHEMY_DATABASE_URL` and environment variables in code to connect to your local MySQL instance.
5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

---

## Application Endpoints

| **Endpoint**       | **Method** | **Description**                                        |
|---------------------|------------|--------------------------------------------------------|
| `/`                | GET        | Homepage rendering the main interface.                |
| `/classify`        | POST       | Upload an image and classify it.                      |
| `/history`         | GET        | View classification history stored in the database.   |

---

## How it Works

1. **Upload Image:** On visiting `/classify`, users can upload images (`JPG`/`PNG`).
2. **Image Preprocessing:** The uploaded image is resized to 64x64, converted to grayscale, and flattened.
3. **Model Prediction:** The pre-trained `smile_classifier.pkl` model predicts if the person is smiling.
4. **Store Classification in DB:** The result and image path are stored in the `history` table in MySQL.
5. **View History:** Users can view previous classifications by visiting the `/history` page.

---

## Environment Variables

These variables are used for the database connection and application:
- `MYSQL_HOST`: MySQL server hostname (default: `mysql_container`)
- `MYSQL_PORT`: MySQL port (default: `3306`)
- `MYSQL_USER`: MySQL username (default: `root`)
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_DB`: MySQL database name (default: `smile_classifier`)

---

## Docker Configuration

The application is fully containerized using `docker-compose.yml`:
- **MySQL Container:** Handles the database for classification history.
- **FastAPI Container:** Runs the classification web app.
- **Network:** Uses a shared Docker bridge network for communication.

---
