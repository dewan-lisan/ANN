## Env setup checklist
```shell
$ env | grep proxy
no_proxy=.sebank.se,localhost,.seb.net,*.sebank.se,*.seb.net,kubernetes.docker.internal
https_proxy=http://wss.sebank.se:80
http_proxy=http://wss.sebank.se:80
```
## Install dependencies
```shell
pip3 config set global.extra-index-url 'https://anonymous@repo7.sebank.se/artifactory/api/pypi/seb-common-pypi/simple'
pip3 config set global.trusted-host 'repo7.sebank.se'
# yes, i know! pypi.python.org should not be used on prod :)
pip3 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org install -r requirements.txt
# pip3 freeze > requirements.txt
```

## Intellij GitBash setup
To activate venv in gitbash terminal, you need to disable automatic activation of virtual environment in Intellij.
Interllij File menu -> Settings -> Tools -> Terminal. Then uncheck "Activate virtualenv". Otherwise it gives "basename: command not found" error

## Intellij test setup checklist
Set run config > working dir: secure-file

## How to run tests
```shell
# setup fortanix api key in the test setup
# export REQUESTS_CA_BUNDLE=<your ca bundle path>
# examples
export REQUESTS_CA_BUNDLE=/c/Users/s86338/ca-certificates.crt
python -m unittest file_decrypter.test.main_test.EndToEndTest.test_run_asymmetric_encrypt
```