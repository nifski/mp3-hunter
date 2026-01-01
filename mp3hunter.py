from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
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
    
    ydl_opts = {
        'quiet': True,
        'nocheckcertificate': True,
        'default_search': 'ytsearch',
        'noplaylist': True,
        'geo_bypass': True,
        'ignoreerrors': True,
    }

    results = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            search_query = f"ytsearch10:{q}"
            info = ydl.extract_info(search_query, download=False)

            if 'entries' in info:
                for video in info['entries']:
                    if not video: continue
                    
                    results.append({
                        "id": video.get('id'),
                        "title": video.get('title', 'UNKNOWN_TITLE'),
                        "author": video.get('uploader', 'UNKNOWN_AUTHOR'),
                        "views": video.get('view_count') or 0,
                        "date": video.get('upload_date', '00000000'),
                        "thumbnail": video.get('thumbnail') or video.get('thumbnails', [{}])[-1].get('url', ''),
                        "url": video.get('webpage_url', '#')
                    })
        except Exception as e:
            return {"error": str(e)}
            
    return results