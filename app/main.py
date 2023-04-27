# Postgres_tutorial
from fastapi import FastAPI, status
from .routers import post, user, authen, vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## we break the code into separate files using ROUTERS
app.include_router(post.router)
app.include_router(user.router)
app.include_router(authen.router)
app.include_router(vote.router)

@app.get('/')
def to_docs():
    return RedirectResponse('/docs', status_code=status.HTTP_307_TEMPORARY_REDIRECT)