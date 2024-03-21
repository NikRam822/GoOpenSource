# GoOpenSource
![logo](docs/media/Logo.png)
## What is GoOpenSource?
Project is a solution to find the right projects for your goals. You can find the right project for your business/research. The platform aggregates projects from multiple sources and allows you to quickly and accurately find the right basis for the realization of your ideas.
## Development

1) **Use Python 3.9.10**: [source](https://www.python.org/downloads/release/python-3910/)
### Start server in production
First you need to create an **.env** file in the root folder of the project and specify the parameter:

```
GITHUB_ACCESS_TOKEN=your_access_token
```

#### Without using a virtual environment: 
In the root directory:

```bash
pip install -r requirements.txt
```

```
python main.py
```

#### For venv
1) Create venv
2) Install requirements and start server. In root directory:
```bash
 pip install -r requirements.txt
 ```
```
python main.py
```
#### Possible Problems:
1) If you have problem with ERROR: Could not install packages due to an OSError - you can try use this:
```
pip install -r requirements.txt --user
```
2) If you fave problem with venv:

```
pip uninstall virtualenv
```
```
pip install virtualenv==20.23.0

```
### Update pip packages
To update pip packages after installing them to the local development environment, run the following commands in root of the project:
```bash
pip freeze > requirements.txt
```
Then don't forget to make a Merge Request with your changes :)
