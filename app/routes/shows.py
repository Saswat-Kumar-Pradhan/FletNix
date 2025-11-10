from fastapi import APIRouter

router = APIRouter(prefix="/shows", tags=["Shows"])

@router.get("/")
def list_shows():
    return {"message": "Shows endpoint will be implemented soon"}
