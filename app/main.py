from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import IdentifyRequest, IdentifyResponse
from app.services import identify_contact
from app.db import get_db, engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bitespeed Identity",
)

@app.post("/identify", response_model=IdentifyResponse, status_code=200)
def identify(payload: IdentifyRequest, db: Session = Depends(get_db)):
    try:
        response = identify_contact(db, payload)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

