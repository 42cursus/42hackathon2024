from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

import dotenv
import nest_asyncio
nest_asyncio.apply()  # This is a workaround for asyncio + claude web retriever

# Load environment variables
dotenv.load_dotenv()

if __name__ == '__main__':
    # from dependencies import get_query_token, get_token_header
    from routers import items, users, files, chat
else:
    from .dependencies import get_query_token, get_token_header
    from .routers import items, users, files, chat

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(title=__name__)

origins = [
    'http://localhost:8080',
    'http://127.0.0.1:8080'
    'http://127.0.0.1:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(chat.router)
app.include_router(items.router)
app.include_router(files.router)

templates = Jinja2Templates(directory="templates/")

@app.get("/")
@app.get("/login")
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

favicon_path = 'favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


# [START run]
if __name__ == '__main__':
    main()

# [END run]
