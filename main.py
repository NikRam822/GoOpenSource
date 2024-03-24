from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ai.repo_keywords import extract_keywords
from api.gitflame_api import GitFlameAPI
from api.github_api import GitHubAPI
from ai.repo_verification import verification_repo
from api.gitlab_api import GitLabAPI
from api.gitverse_api import GitVerseAPI
from api.moshub import MosHub

origins=[
    "http://localhost:5173",

]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Accept",
                   "Access-Control-Allow-Origin",
                   "Content-Length",
                   "Accept-Encoding",
                   "X-CSRF-Token",
                   "Authorization",
                   "Content-Type",
                   "Access-Control-Expose-Headers",
                   "Access-Control-Allow-Headers",
                   "Set-Cookie"]
)

apis = {
    "GitHubAPI": GitHubAPI(),
    "GitLabAPI": GitLabAPI(),
    "GitFlameAPI": GitFlameAPI(),
    "MosHub": MosHub(),
    "GitVerseAPI": GitVerseAPI(),
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

    keywords = extract_keywords(query)

    all_repos = []
    for keyword in keywords:
        print(keyword, end=' ')
        for name, api in apis.items():
            print(name, end=' ')
            repos = api.get_repositories(keyword)
            all_repos.extend(repos)
        print(len(all_repos))
        # middleware for AI solutions

    seen = set()
    verification_repo([repo for repo in all_repos if repo.link not in seen and not seen.add(repo.link)],
                      query)
    # print(f"Repositories from {name}: {repos}")

    all_repos.sort(key=lambda repo: repo.stars, reverse=True)

    result = [x.link for x in all_repos]

    return {"repositories": [result]}


if __name__ == '__main__':
    # python main.py - for start server in prod
    uvicorn.run(app, host="127.0.0.1", port=8000)
