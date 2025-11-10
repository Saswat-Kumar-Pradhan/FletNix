from fastapi import FastAPI, Query, HTTPException, Depends
from bson import ObjectId
from typing import Optional
from app.database import shows_collection
from app.auth import auth_router
from app.imdb import fetch_imdb_reviews

app = FastAPI(title="FletNix API")
app.include_router(auth_router)

# 🧾 List all shows (search + pagination + filters + age restriction)
@app.get("/shows")
def get_shows(
    page: int = 1,
    limit: int = 15,
    search: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    age: Optional[int] = Query(None)
):
    skip = (page - 1) * limit
    query = {}

    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"cast": {"$regex": search, "$options": "i"}}
        ]
    if type:
        query["type"] = {"$regex": f"^{type}$", "$options": "i"}
    if age and age < 18:
        query["rating"] = {"$ne": "R"}

    cursor = shows_collection.find(query).skip(skip).limit(limit)
    shows = []
    for s in cursor:
        s["_id"] = str(s["_id"])
        shows.append(s)

    total = shows_collection.count_documents(query)
    return {"page": page, "total": total, "results": shows}

# 📄 Show details with IMDB reviews + recommendations
@app.get("/shows/{show_id}")
def get_show_detail(show_id: str):
    show = shows_collection.find_one({"_id": ObjectId(show_id)})
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    show["_id"] = str(show["_id"])

    # Fetch IMDb reviews dynamically
    imdb_data = fetch_imdb_reviews(show.get("title", ""))
    show["imdb"] = imdb_data

    # Genre-based recommendations
    genre = show.get("listed_in", "").split(",")[0] if show.get("listed_in") else None
    recs = []
    if genre:
        rec_cursor = shows_collection.find(
            {"listed_in": {"$regex": genre, "$options": "i"}, "_id": {"$ne": ObjectId(show_id)}}
        ).limit(5)
        recs = [{"_id": str(r["_id"]), "title": r["title"], "type": r["type"]} for r in rec_cursor]

    show["recommendations"] = recs
    return show
