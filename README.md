# ![](teleios.png)

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

## Prerequisites
Here is what you need to install the software.

1. Git 

To fetch the source code you'll require [git](https://git-scm.com/) to be installed on your machine.

```
$ git clone https://gitlab.com/arnoldnderitu1/teleios.git
```

2. Python

Teleios requires Python 3.6 or later to run. Use your package manager to download and install python 3 on your machine if you don't have it already.
> If Python 3 is already installed, make sure that the version is 3.6 or above 
```
$ python3 --version
```
> Verify that [pip](https://pip.pypa.io/) is installed for this version.
```
$ pip3 --version
```

3. Dependencies 
Project dependencies are listed in the `requirements.txt` file located at the root of the Teleios directory
> It is preferable to not to mix python modules packages within your system. You can use [virtualenv](https://pypi.python.org/pypi/virtualenv) to create isolated Python environments

Navigate to the path of the Teleios root directory and run pip on the requirements file:
```
$ cd /teleios
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

4. Initialize Database

For demo, initialize and seed the DB with data:
```
$ flask db upgrade
$ flask deploy
```

## Running Teleios
Once all dependencies are set up, to launch the app in debug mode:
```
$ export FLASK_DEBUG=1
$ flask run
```

Navigate to http://127.0.0.1:5000/ on your local browser

## Credentials
To log in as admin:

> **Email**:admin<br>
> **Password**: admin
