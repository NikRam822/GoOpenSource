# GoOpenSource
## What is GoOpenSource?
Project is a solution to find the right projects for your goals. You can find the right project for your business/research. The platform aggregates projects from multiple sources and allows you to quickly and accurately find the right basis for the realization of your ideas.
## Development

Python 3.9

### Start server in production
First you need to create an **.env** file in the root folder of the project and specify the parameter:

```
GITHUB_ACCESS_TOKEN=your_access_token
```
In the root directory:
```bash
pip install -r requirements.txt
```

```
python main.py
```
#### Possible Problems:
If you have problem with ERROR: Could not install packages due to an OSError - you can try use this:
```
pip install -r requirements.txt --user
```
### Update pip packages
To update pip packages after installing them to the local development environment, run the following commands in root of the project:
```bash
pip freeze > requirements.txt
```
Then don't forget to make a Merge Request with your changes :)