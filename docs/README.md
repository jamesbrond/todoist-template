# todoist-template

> Easily add tasks to Todoist with customizable templates.

The aim of this project is to facilitate the creation of tasks on the Todoist platform thanks to simple templates.

A template is nothing more than a file written in YAML whose structure reflects the hierarchy Project - Session (optional) - Task.
Projects, sessions and labels are automatically created if they do not already exist on your Todoist.

Todoist templates always create a new project, while the big difference here is that with todoist-template you can add tasks to existing projects or to the Inbox.
Another difference is the ability to parameterize templates. For example, by passing parameters from the command line, you can create tasks with custom due date.

## Installing / Getting started

### Before you start

Ensure that the following prerequisites are met:

- You have installed Python. If you're using macOS or Linux, your computer already has Python installed. You can get Python from [python.org](http://python.org/download/).

- Next step is to install and activate a Python virtual environments. It allow you to install Python packages in an isolated location from the rest of your system instead of installing them system-wide.
There are multiple reasons why virtual environments are a good idea and these are also the reason why I’m telling you about them before we continue to the part where we start installing 3rd party packages.

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

### Authorization token

todoist-template uses Todoist REST API, in order to make authorized calls, you must provide the [Todoist authorization token](https://developer.todoist.com/rest/v1/?python#next-steps).

When you run todoist-template for the first time, the application will ask you for the Todoist authorization token and it will be stored in the system keyring service.
These keyring backends are supported:

- macOS Keychain
- Freedesktop Secret Service supports many IDE including GNOME (requires secretstorage)
- KDE4 & KDE5 KWallet (requires dbus)
- Windows Credential Locker

To use todoist-template with different authorization tokens use the `--id` arguments (see [Run todoist-template](./README.md#run-todoist-template)).

### Run todoist-template

```shell
python todoist-template.py [options]
```

Where options are:

| Option                   | Default   | Description                                    |
|--------------------------|-----------|------------------------------------------------|
| TEMPLATE                 | stdin     | Mandatory path to the YAML template file       |
| -h, --help               |           | Show help message and exit                     |
| -D KEY0=VAL0,KEY1=VAL1...|           | The placeholder values replaced in template    |
| --id SERVICE_ID          | TODOIST-TEMPLATE | Keyring service name where store Todoist API Token |
| --version                |           | Show program's version number and exit         |
| -d, --debug              | False     | More verbose output. Default log level is INFO |
| -q, --quiet              | False     | Suppress output                                |

Example

```shell
python todoist-template.py -d templates/simple_template0.yml
```

Run todoist-template from different users specify differnet keyring service name:

```shell
python todoist-template.py [options] --id JHON-TOKENS
```

```shell
python todoist-template.py [options] --id MARY-TOKENS
```

You can use standar input to provide the template to todoist-template:

```shell
python todoist-template.py -d < templates/simple_template0.yml
```

## Template

To learn how to write and use templates please read the template examples:

[Simple template](./template/simple_template.md)
> Basic template

[Parameterized template](./template/param_template.md)
> Template with placeholder replaced runtime

[Complex template](./template/complex_template.md)
> Templete with multiple projects and sections

[Inlcude templates](./template/include_template.md)
> Include templates to create a more complex template

## Developing

See [our developing guide](./DEVELOPING.md)

## Contributing

See [our contributing guide](./CONTRIBUTING.md).

## Links

- Project homepage: <https://jamesbrond.github.com/todoist-template/>
- Repository: <https://github.com/jamesbrond/todoist-template/>
- Issue tracker: <https://github.com/jamesbrond/todoist-template/issues>

## Licensing

See [license](../LICENSE)
