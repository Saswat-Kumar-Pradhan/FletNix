from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from typing import Optional
from app.database import shows_collection
from app.auth import auth_router
from app.imdb import fetch_imdb_reviews


app = FastAPI(title="FletNix API")

# 🧩 Enable CORS (for local + Vercel frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can later restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Authentication routes
app.include_router(auth_router)


# 🧾 List all shows (search + pagination + filters + age restriction)
@app.get("/shows")
def get_shows(
    page: int = 1,
    limit: int = 15,
    search: Optional[str] = Query(None, description="Search by title or cast"),
    type: Optional[str] = Query(None, description="Filter by type: Movie or TV Show"),
    age: Optional[int] = Query(None, description="Filter content based on age")
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

    if age is not None and age < 18:
        query["rating"] = {"$ne": "R"}

    cursor = shows_collection.find(query).skip(skip).limit(limit)
    shows = []
    for s in cursor:
        s["_id"] = str(s["_id"])
        shows.append(s)

    total = shows_collection.count_documents(query)
    return {"page": page, "total": total, "results": shows}


# 📄 Show details with IMDb reviews + genre-based recommendations
@app.get("/shows/{show_id}")
def get_show_detail(show_id: str):
    try:
        show = shows_collection.find_one({"_id": ObjectId(show_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid show ID")

    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    show["_id"] = str(show["_id"])

    # 🎬 Fetch IMDb reviews dynamically
    imdb_data = fetch_imdb_reviews(show.get("title", ""))
    show["imdb"] = imdb_data

    # 🎭 Genre-based recommendations
    genre = show.get("listed_in", "").split(",")[0].strip() if show.get("listed_in") else None
    recs = []
    if genre:
        rec_cursor = shows_collection.find(
            {
                "listed_in": {"$regex": genre, "$options": "i"},
                "_id": {"$ne": ObjectId(show_id)}
            }
        ).limit(5)
        recs = [{"_id": str(r["_id"]), "title": r["title"], "type": r["type"]} for r in rec_cursor]

    show["recommendations"] = recs
    return show


# 🌐 Root route for health check
@app.get("/")
def root():
    return {"message": "Welcome to FletNix API"}


# ⚙️ Only used for local development (Vercel ignores this)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
