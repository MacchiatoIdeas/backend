Macchiato: Appunta Backend
==========================

## Set up a Development Environment

Please follow these steps so we all have the same working environment, and you avoid confusion.

- Make sure that `git config --global user.name` and `git config --global user.email` retrieve your credentials, otherwise execute those command and append the desired value.
- Install Python 3, at the moment we haven't set a specific minor-patch version.
- Install virtualenv for Python 3, on fedora the command should be virtualenv-3, on MacOS can be installed with pip or brew.

- In a directory of your preference, create a directory named "macchiato", which will hold all our project repositories.
- Execute: `git clone git@github.com:MacchiatoIdeas/backend.git`
- Enter to the recently created directory.
- Execute: `virtualenv -p python3 venv`, this will create a venv directory with python 3.
- Execute: `. venv/bin/activate` to activate the virtualenv.
- To ensure that everything is installed correctly execute: `which python`, the returned string should point to the venv path. Do the same for `virtualenv`.
- Install dependencies with: `pip install -r requirements.txt`.
- If something fails leave a detailed issue.

## Back to Code

Everytime you come back to code, execute:

```
git pull
. venv/bin/activate
```

If the `requirements.txt` file changed, install the missing dependencies.

If at any point you need to add a dependency with pip, execute: `pip freeze`, check that you only have dependencies that THE PROJECT needs, and then `pip freeze > requirements.txt` to save. Lastly commit and push.
