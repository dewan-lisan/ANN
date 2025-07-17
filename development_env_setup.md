## Install dependencies
```shell
pip3 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org install -r requirements.txt
# pip3 freeze > requirements.txt
```

## Intellij GitBash setup
To activate venv in gitbash terminal, you need to disable automatic activation of virtual environment in Intellij.
Interllij File menu -> Settings -> Tools -> Terminal. Then uncheck "Activate virtualenv". Otherwise it gives "basename: command not found" error
