from datetime import datetime
from bson.objectid import ObjectId

from fastapi import APIRouter, Form

from app.utils.mongodb import fetch_documents, update_document, delete_document

from app.langchain.langgraph_main import langgraph_app
from app.schemas.schemas import Message, Role
from app.langchain.common import Documents


router = APIRouter()


@router.get("/")
def root():
    return {"message": "/conversation/ route working fine"}


@router.post("/chat")
def reply_to_message(
    user_id: str = Form(...),
    vendor_id: str = Form(...),
    review_id: str = Form(...),
    user_msg: str = Form(...),
    test: str = Form("false"),
    reset: str = Form("false"),
):
    test = test.lower() == "true"
    reset = reset.lower() == "true"

    if reset:
        delete_document(review_id)

    documents: Documents = fetch_documents(review_id, user_id, vendor_id)
    print(documents)
    print(documents.review)    
    print(type(documents.review))

    documents.add(
        Message(
            role=Role.USER,
            content=user_msg,
        )
    )

    documents = langgraph_app.invoke(documents)

    was_update_successful = update_document(
        review_id, user_id, vendor_id, documents
    )

    if not was_update_successful:
        return {"message": "updating MongoDB failed"}

    reply = documents["state"].get("reply_message", "No reply message found")

    return {"message": reply}
