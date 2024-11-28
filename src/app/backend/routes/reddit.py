from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.app.backend.reddit.reddit import RedditScrapper
from pydantic import BaseModel
from src.app.backend.workspaces.models import WorkspaceReq, WorkspaceProperties
from src.app.backend.auth.utils import get_current_user
from src.app.backend.auth.utils import logger

router = APIRouter()


class SubredditModel(BaseModel):
    name: str


@router.post("/get_all_post")
async def scrape_subreddit(sub: SubredditModel):
    rs = RedditScrapper(sub.name)
    posts = rs.get_all_posts_from_subreddit()
    if posts:
        return {"number": f"{len(posts)}"}
    else:
        raise HTTPException(
            status_code=400, detail=f"Problem getting posts for subreddit {sub.name} "
        )
