# todoist-template

> Easily add tasks to Todoist with customizable templates.

The aim of this project is to facilitate the creation of tasks on the Todoist
platform thanks to simple templates.

A template is nothing more than a file written in YAML or JSON whose structure
reflects the hierarchy Project - Session (optional) - Task.
Projects, sessions and labels are automatically created if they don't already
exist on your Todoist.

Todois.com templates always create a new project, while the big difference here
is that with todoist-template you can add tasks to existing projects or to the
Inbox.
Another difference is the ability to parameterize templates. For example, by
passing parameters from the command-line, you can create tasks with custom due
date.
Anyway todoist-template can also import Todoist.com CSV templates.

## Installing / Getting started

Before you start check the [prerequisite and install instructions](install.md).

### Authorization token

todoist-template uses Todoist REST API, in order to make authorized calls, you
must provide the [Todoist authorization token](
https://developer.todoist.com/rest/v1/?python#next-steps).

When you run todoist-template for the first time, the application will ask you
for the Todoist authorization token and it will be stored in the system
keyring service.
These keyring backends are supported:

- macOS Keychain
- Freedesktop Secret Service supports many IDE including GNOME (requires
secretstorage)
- KDE4 & KDE5 KWallet (requires dbus)
- Windows Credential Locker

To use todoist-template with different authorization tokens use the `--id`
arguments (see [Run todoist-template](./README.md#run-todoist-template)) or
specify `--token` argument.

### Run todoist-template

```shell
python todoist-template.py [options]
```

Where options are:

| Option                   | Default   | Description                                               |
|--------------------------|-----------|-----------------------------------------------------------|
| TEMPLATE                 | stdin     | Mandatory path to the YAML or JSON template file          |
| -h, --help               |           | Show help message and exit                                |
| -D KEY0=VAL0,KEY1=VAL1...|           | The placeholder values replaced in template or the CSV file |
| --id SERVICE_ID          | TODOIST-TEMPLATE | Keyring service name where store Todoist API Token |
| --version                |           | Show program's version number and exit                    |
| -d, --debug              | False     | More verbose output. Default log level is INFO            |
| -q, --quiet              | False     | Suppress output                                           |
| --dry-run                | False     | Allows the `todoist-template` command to run a trial without making any changes on Todoist.com, this process has the same output as the real execution except for new object IDs. |
| -u, --update             |           | it updates task with the same name instead of adding a new one |
| --undo UNDOFILE          |           | Loads undo file and rollbacks all operations in it        |
| --token API_TOKEN        |           | The Todoist authorization token. It will use this token instead of reading it from Keyring service |
| --gui                    |           | Start Todoist-Template service with web frontend          |

Example

```shell
python todoist_template.py -d templates/simple_template0.yml
```

Run todoist-template from different users specify differnet keyring service name:

```shell
python todoist_template.py [options] --id JHON-TOKENS
```

```shell
python todoist_template.py [options] --id MARY-TOKENS
```

You can use standar input to provide the template to todoist-template:

```shell
python todoist_template.py -d < templates/simple_template0.yml
```

### Undo

todoist-template produces a undo output file. You can use it to delete all
created objects and revert all modified ones. For example:

```shell
python todoist_template.py --undo simple_template0-20220808081215.undo
```

The undo file is named as `template_file_name-YYYYmmddHHMMSS.undo`.

## Template

To learn how to write and use templates please read the template examples:

[Simple template](./template/simple_template.md)
> Basic template

[Parameterized template](./template/param_template.md)
> Template with placeholder replaced runtime

[Complex template](./template/complex_template.md)
> Templete with multiple projects and sections and sub-tasks

[Inlcude templates](./template/include_template.md)
> Include templates to create a more complex template

## Developing

See [our developing guide](./DEVELOPING.md)

## Contributing

See [our contributing guide](./CONTRIBUTING.md).

## Security Policies and Procedures

See [our security policies and procedures guidelines](./SECURITY.md).

## Links

- Project homepage: <https://jamesbrond.github.com/todoist-template/>
- Repository: <https://github.com/jamesbrond/todoist-template/>
- Issue tracker: <https://github.com/jamesbrond/todoist-template/issues>

## Licensing

See [license](../LICENSE)
