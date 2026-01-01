from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from youtubesearchpython import VideosSearch
import uvicorn
import os

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

@app.get("/search")
def search_youtube(q: str):
    print(f"SCANNING_NETWORK_FOR: {q}")
    
    try:
        videos_search = VideosSearch(q, limit=10)
        results_dict = videos_search.result()
        
        clean_results = []
        
        for video in results_dict.get('result', []):
            
            thumbnails = video.get('thumbnails', [])
            thumb_url = thumbnails[-1]['url'] if thumbnails else ''
            
            view_text = video.get('viewCount', {'text': '0'})['text']
            import re
            views_numeric = re.sub(r'[^\d]', '', view_text)
            views_numeric = int(views_numeric) if views_numeric else 0
            
            clean_results.append({
                "id": video.get('id'),
                "title": video.get('title', 'UNKNOWN_TITLE'),
                "author": video.get('channel', {}).get('name', 'UNKNOWN_AUTHOR'),
                "views": views_numeric,
                "date": video.get('publishedTime', 'N/A'),
                "thumbnail": thumb_url,
                "url": video.get('link', '#')
            })
            
        return clean_results

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))