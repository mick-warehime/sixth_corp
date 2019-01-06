# sixth_corp


## PyCharm Setup

### Project Structure

Set the source code directories in the preferences. 

PyCharm > Preferences > Project: sixth_corp > Project Structure

* src
* sample
* Any additional directories that get added (also add a __init__.py)

### Test Runner - Unittest

Set the default test runner to be Unittest 

PyCharm > Preferences > Tools > Python Integrated Tools

* Testing > Default Test Runner
* Select "Unittest"

### Run Configurations

I use 3 run configurations 
1) main app
2) unittests only (fast)
3) unittests, style (flake8) and static type checks (mypy) (slow)

#### Main App

* Working Directory: [path to project]/sixth_corp
* Script Path: [path to project]/sixth_corp/src/app.py

#### Unitests Only (fast)

* Target: [path to project]/sixth_corp/src
* Additional Arguments: -p "*_test.py"
* Working Directory: [path to project]/sixth_corp/src

#### Unitests, Style + Types (slow)

Copy the Unitests Only configuration to a new configuration and rename it. Then set up the three following external tools to run (order is important).

* Run external tool (autopep8) - automatically corrects pep8 issues
    * Program: autopep8
    * Arguments: -max-line-length 100
    * Working Directory: $ProjectFileDir$
* Run external tool (flake8) - detects additional pep8/style issues not caught by autopep8
    * Program: /usr/local/bin/flake8
    * Arguments: -exclude src/app.py
    * Working Directory: $ProjectFileDir$
* Run external tool (mypy) - static type checker
    * Program: /usr/local/bin/mypy
    * Arguments: -p src --ignore-missing-imports
    * Working Directory: $ProjectFileDir$
* Run external tool (isort) - sorts python import lines automatically
    * pip install isort
    * Program: isort
    * Arguments: -rc -y
    * Working Directory: $ProjectFileDir$
        



