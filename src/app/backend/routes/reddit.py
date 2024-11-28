from fastapi import APIRouter
from src.app.backend.reddit.reddit import RedditScrapper


router = APIRouter()


@router.post("/scrape_subreddit")
async def scrape_subreddit():
    pass
