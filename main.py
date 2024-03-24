from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ai.readme_analyze import ReadMeAnalyzer
from ai.repo_keywords import Query
from api.gitflame_api import GitFlameAPI
from api.github_api import GitHubAPI
from ai.repo_verification import verification_repo
from api.gitlab_api import GitLabAPI
from api.gitverse_api import GitVerseAPI
from api.moshub import MosHub

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
    "http://0.0.0.0:5173",
    "http://0.0.0.0:8000",
    "http://0.0.0.0",
    "http://10.129.0.29:8000",
    "http://10.129.0.29:5173",
    "http://10.129.0.29",
    "http://158.160.19.38:5173",
    "http://158.160.19.38:8000",
    "http://158.160.19.38"
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

    query = Query(user_query=query)
    keywords = query.get_key_queries_from_correct_query().split(',')
    print(keywords)

    readme_analyzer = ReadMeAnalyzer(query)

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
    unique_repos = [repo for repo in all_repos if repo.link not in seen and not seen.add(repo.link)]
    # print(f"Repositories from {name}: {repos}")

    if len(unique_repos) == 0:
        return {"repositories": []}

    out_meta, out_description, out_rating = readme_analyzer.analyze_readme(unique_repos)

    # print(f"Repositories from {name}: {repos}")

    for i in range(len(out_meta)):
        unique_repos[i].out_rating = (1 - out_rating[i]) * 100
        unique_repos[i].out_description = out_description[i]

    unique_repos.sort(key=lambda repo: (repo.out_rating, repo.stars), reverse=True)

    result = [x.link for x in unique_repos]

    return {"repositories": [unique_repos]}


if __name__ == '__main__':
    # python main.py - for start server in prod
    uvicorn.run(app, host="127.0.0.1", port=8000)
