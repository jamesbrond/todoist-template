# Installing / Getting started

## Before you start

- You have installed Python. If you're using macOS or Linux, your computer already has Python installed. You can get Python from [python.org](http://python.org/download/).

- Next step is to install and activate a Python virtual environments. It allow you to install Python packages in an isolated location from the rest of your system instead of installing them system-wide.
There are multiple reasons why virtual environments are a good idea and these are also the reason why I’m telling you about them before we continue to the part where we start installing third-party packages.

  - Preventing version conflicts
  - Easy to reproduce and install
  - Works everywhere, even when not root

  There are several ways to create a Python virtual environment, depending on the Python version you are running.
  If you are running Python 3.4+, you can use the venv module baked into Python:

  ```shell
  python -m venv venv
  ```

  How you activate your virtual environment depends on the OS you’re using.
  To activate your venv on Windows, you need to run a script that gets installed by venv. If you created your venv in a directory called myenv, the command would be:

  ```shell
  # In cmd.exe
  venv\Scripts\activate.bat
  # In PowerShell
  venv\Scripts\Activate.ps1
  ```

  On Linux and MacOS, we activate our virtual environment with the source command. If you created your venv in the myvenv directory, the command would be:

  ```shell
  source venv/bin/activate
  ```

- Finally before running the todoist-template script you have to install Python packages with the Pip package manager.

  The `requirements.txt` file contains the list of dependencies. To install all the dependencies listed in this file, use:

  ```shell
  pip install -r requirements.txt
  ```
