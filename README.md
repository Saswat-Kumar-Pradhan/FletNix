# 🎬 FletNix – What to Watch

**FletNix** is a Netflix-style movie and TV show discovery platform built with **FastAPI** and **MongoDB Atlas**.  
It allows users to browse, search, and filter Netflix titles with age restrictions, authentication, and genre-based recommendations.

---

## 🧭 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🧩 Overview

This backend powers the FletNix Angular frontend — providing authentication,  
movie browsing, recommendations, and IMDb reviews dynamically.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | FastAPI (Python 3.9+) |
| **Database** | MongoDB Atlas |
| **Auth** | JWT, bcrypt |
| **External API** | OMDB API (for IMDb ratings & reviews) |
| **Frontend (separate)** | Angular 12+ with Tailwind CSS |
| **Hosting** | Vercel |

---

## 🚀 Features

| Feature | Description |
|----------|-------------|
| 🔐 **Authentication** | Register/Login with hashed passwords & JWT |
| 🎞️ **Paginated List** | Paginate through all titles (15 items/page) |
| 🔎 **Search** | Search by title or cast |
| ⚖️ **Age Restriction** | Under 18 users can’t see R-rated content |
| 🎬 **Filter by Type** | Filter Movies or TV Shows |
| 🧾 **Detail Page** | Get all info about a show |
| ⭐ **IMDb Reviews** | Dynamic IMDb rating & top reviews |
| 🎭 **Genre Recommendations** | Auto-recommend related shows |
| 🧱 **Clean API Design** | RESTful endpoints with query filters |
| 🧪 **Testing Ready** | Works with Playwright / pytest |
| 🖥️ **Responsive UI (Frontend)** | Tailwind CSS (Angular side) |

---

## 🗂️ Project Structure

