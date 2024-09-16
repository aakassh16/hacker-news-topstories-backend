from fastapi import FastAPI, HTTPException
import requests, os, uvicorn
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS Management
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hacker-news-topstories.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
HACKER_NEWS_API_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


@app.get("/top-stories")
async def get_top_stories():
    try:
        response = requests.get(HACKER_NEWS_API_URL)
        response.raise_for_status() 
        story_ids = response.json()[:10]  # 10 Stories only

        stories = []
        for story_id in story_ids:
            story_data = requests.get(STORY_URL.format(story_id)).json()
            story = {
                "title": story_data.get("title", "No Title"),
                "author": story_data.get("by", "Unknown"),
                "url": story_data.get("url", "#"),
                "score": story_data.get("score", 0),
                "time": datetime.fromtimestamp(story_data.get("time", 0)).strftime('%Y-%m-%d %H:%M:%S')
            }
            stories.append(story)
        print(stories)
        return stories
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="HackerNews API is unreachable") from e

# For Reneder Deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)