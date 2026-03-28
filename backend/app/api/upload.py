import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional

from ..db.duckdb_client import CSVReader

router = APIRouter(prefix="/api/csv", tags=["csv"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")

    with open(file_path, "wb") as f:
        f.write(contents)

    info = CSVReader.load_csv(file_path)

    columns_info = []
    for col in info["columns"]:
        columns_info.append({"name": col, "data_type": "unknown", "sample_values": []})

    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": len(contents),
        "path": file_path,
        "columns": columns_info,
        "row_count": info["row_count"],
    }
