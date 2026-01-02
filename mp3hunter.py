from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from youtube_search import YoutubeSearch
from fastapi.responses import FileResponse

import uvicorn
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    return FileResponse('index.html')
    
@app.get("/favicon.ico")
async def favicon():
    return FileResponse('favicon.ico')

@app.get("/search")
def search_youtube(q: str):
    print(f"SCANNING_NETWORK_FOR: {q}")
    
    try:
        results = YoutubeSearch(q, max_results=50).to_dict()
        
        clean_results = []
        
        for video in results:
            video_url = f"https://www.youtube.com{video.get('url_suffix')}"
            
            raw_views = video.get('views', '0')
            import re
            views_numeric = re.sub(r'[^\d]', '', raw_views)
            views_numeric = int(views_numeric) if views_numeric else 0
            
            thumb = video.get('thumbnails', [None])[0]
            if isinstance(thumb, str):
                thumb_url = thumb
            else:
                thumb_url = f"https://i.ytimg.com/vi/{video.get('id')}/hqdefault.jpg"

            clean_results.append({
                "id": video.get('id'),
                "title": video.get('title', 'UNKNOWN_TITLE'),
                "author": video.get('channel', 'UNKNOWN_AUTHOR'),
                "views": views_numeric,
                "date": video.get('publish_time', 'N/A'),
                "thumbnail": thumb_url,
                "url": video_url
            })
            
        return clean_results

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))