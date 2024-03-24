from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.gitflame_api import GitFlameAPI
from api.github_api import GitHubAPI
from ai.repo_verification import verification_repo
from api.gitlab_api import GitLabAPI
from api.gitverse_api import GetVerseAPI
from api.moshub import MosHub

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

apis = {
    "GitHubAPI": GitHubAPI(),
    "GitLabAPI": GitLabAPI(),
    "GitFlameAPI": GitFlameAPI(),
    "MosHub": MosHub(),
    "GetVerseAPI": GetVerseAPI(),
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
    # TODO: AI FOR BUILD QUERY FOR GITHUB
    all_repos = []
    result = []
    for name, api in apis.items():
        repos = api.get_repositories(query)
        all_repos.append(repos)
        # middleware for AI solutions
        verification_repo(repos, query)
        # print(f"Repositories from {name}: {repos}")
        result.append(x.link for x in repos)

    return {"repositories": result}


if __name__ == '__main__':
    # python main.py - for start server in prod
    uvicorn.run(app)
