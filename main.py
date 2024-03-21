from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.github_api import GitHubAPI
from ai.repo_verification import verification_repo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

apis = {
    "GitHubAPI": GitHubAPI()
}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/getRepositories")
async def read_item(request: Request):
    data = await request.json()
    query = data.get('queryForProject')

    all_repos =[]
    for name, api in apis.items():
        repos = api.get_repositories(query)
        all_repos.append(repos)
        # middleware for AI solutions
        verification_repo(repos, query)
        print(f"Repositories from {name}: {repos}")
    return {"repositories" : all_repos}

if __name__ == '__main__':
    # python main.py - for start server in prod
    uvicorn.run(app, host='127.0.0.1', port=8000)
