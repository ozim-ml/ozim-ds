# main.py
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.read_file import *
from pydantic import BaseModel
import os

app = FastAPI()

current_directory = os.path.dirname(os.path.realpath(__file__))
static_folder = os.path.join(current_directory, "static")
templates_folder = os.path.join(static_folder, "templates")

app.mount("/static", StaticFiles(directory=static_folder), name="static")
templates = Jinja2Templates(directory=templates_folder)

class ColumnSelection(BaseModel):
    index_column: str
    target_column: str

start_df = None
temp_df = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/data_selection", response_class=HTMLResponse)
async def data_selection(request: Request):
    return templates.TemplateResponse("data_selection.html", {"request": request})

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    global start_df, temp_df
    try:
        start_df = await read_file_to_df(file)
        temp_df = start_df.copy()
        return JSONResponse(content={"filename": file.filename, "columns": start_df.columns.tolist()})
    except ValueError as e:
        return {"error": str(e)}

@app.post("/set_columns")
async def choose_columns(column_selection: ColumnSelection):   
    global temp_df, start_df

    if start_df is None:
        return {"error": "Data not uploaded or failed to load"}

    # Check if the columns exist in the original dataframe
    if column_selection.index_column not in start_df.columns:
        return {"error": "Index column not found"}

    if column_selection.target_column not in start_df.columns:
        return {"error": "Target column not found"}

    # Create a fresh copy of start_df to modify
    temp_df = start_df.copy()

    # Set the new index and rename the target column
    temp_df.set_index(column_selection.index_column, inplace=True)
    temp_df = temp_df.rename(columns={column_selection.target_column: 'target'})

    return {"message": "Columns set successfully"}