import json
import random
import string
import aiofiles

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from typing import Annotated
app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get("/")
async def index(request:Request):
    return templates.TemplateResponse(request=request, name='index.html')

@app.post("/")
async def get_url(url: Annotated[str, Form()]):
    shot_url = ''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for _ in range(6))

    async with aiofiles.open('filename', mode='r') as f:
        contents = await f.read()
    db_dict = json.loads(contents)

    db_dict[shot_url] = url

    async with aiofiles.open('filename', mode='w') as f:
        await f.write(json.dumps(db_dict))

    return {'result': shot_url}


@app.get("/{short_url}")
async def say_hello(short_url: str):
    async with aiofiles.open('filename', mode='r') as f:
        contents = await f.read()
        db_dict = json.loads(contents)
        url = db_dict[short_url]

    return RedirectResponse(url)
