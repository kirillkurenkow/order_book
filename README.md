# Project for CQG interview

## How to run tests
### Install requirements
You can install requirements by executing this from project directory
```cmd
pip install -r requirements.txt
```

### Check defaults config
To change default test values you can check out [defaults.cfg](/Tests/Resource/defaults.cfg)

### Run tests
You can run tests from [Tests](/Tests) directory

Just run all tests
```cmd
pytest
```
Run tests with report
```cmd
pytest --alluredir {reports_dir}
```
Run positive or negative tests
```cmd
pytest -m {positive|neagative}
```

### View report
```cmd
allure serve {reports_dir}
```
