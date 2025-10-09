<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Todoist-Template</h3>

  <p align="center">
    Easily add tasks to Todoist with customizable templates!
    <br />
    <br />
    <a href="https://github.com/jamesbrond/todoist-template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/jamesbrond/todoist-template/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a> 
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#authorization-token">Authorization token</a></li>
        <li><a href="#run-todoist-template">Run todoist-template</a></li>
        <li><a href="#undo">Undo</a></li>
      </ul>
    </li>
    <li><a href="#template">Template</a></li>
    <li><a href="#developing">Developing</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#security-policies-and-procedures">Security Policies and Procedures</a></li>
    <li><a href="#links">Links</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The aim of this project is to facilitate the creation of tasks on the Todoist
platform thanks to simple templates.

A template is nothing more than a file written in YAML or JSON whose structure
reflects the hierarchy Project - Session (optional) - Task.
Projects, sessions and labels are automatically created if they don't already
exist on your Todoist.

Todoist.com templates always create a new project, while the big difference here
is that with todoist-template you can add tasks to existing projects or to the
Inbox.
Another difference is the ability to parameterize templates. For example, by
passing parameters from the command-line, you can create tasks with custom due
date.
Anyway todoist-template can also import Todoist.com CSV templates.

## Getting started

Before you start check the [prerequisite and install instructions](install.md).

### Authorization token

todoist-template uses Todoist REST API, in order to make authorized calls, you
must provide the [Todoist authorization token](https://developer.todoist.com/rest/v1/?python#next-steps).

When you run todoist-template for the first time, the application will ask you
for the Todoist authorization token and it will be stored in the system
keyring service.
These keyring backends are supported:

- macOS Keychain
- Freedesktop Secret Service supports many IDE including GNOME (requires
  secret storage)
- KDE4 & KDE5 KWallet (requires dbus)
- Windows Credential Locker

To use todoist-template with different authorization tokens use the `--id`
arguments (see [Run todoist-template](./README.md#run-todoist-template)) or
specify `--token` argument.

### Run todoist-template

```shell
python todoist_template.py [options]
```

Where options are:

| Option | Default | Description |
| - | - | - |
| TEMPLATE | stdin | Mandatory path to the YAML, JSON or CSV template |
| -h, --help | | Show help message and exit |
| -D KEY0=VAL0,KEY1=VAL1... | | The placeholder values replaced in template or the CSV file |
| --id SERVICE_ID | TODOIST-TEMPLATE | Keyring service name where store Todoist API Token |
| --version | | Show program's version number and exit |
| -c, --config | CONFIGFILE| TOML configuration file (default: `lib/config/config.toml`) |
| -d, --debug | False | More verbose output. Default log level is INFO |
| -q, --quiet | False | Suppress output |
| --dry-run | False | Allows the `todoist_template` command to run a trial without making any changes on Todoist.com, this process has the same output as the real execution except for new object IDs. |
| -u, --update | | it updates task with the same name instead of adding a new one                                                                                                                    |
| --undo UNDOFILE | | Loads undo file and rollbacks all operations in it |
| --token API_TOKEN | | The Todoist authorization token. It will use this token instead of reading it from Keyring service |
| -t | False | Adds a new item using the Todoist Quick Add implementation, the template will be used as text for the new task |
| --yaml | | template input file has YAML format |
| --json | | template input file has JSON format |
| --csv | | template input file has CSV format |

Example

```shell
python todoist_template.py -d templates/simple_template0.yml
```

Run todoist-template from different users specify different keyring service name:

```shell
python todoist_template.py [options] --id JOHN-TOKENS
```

```shell
python todoist_template.py [options] --id MARY-TOKENS
```

You can use standard input to provide the template to todoist-template:

```shell
python todoist_template.py -d < templates/simple_template0.yml
```

Example of adding a new task with the Todoist Quick Add implementation:

```shell
echo -e "test quick add {day}" | python todoist_template.py -t -D day=tod
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

> Template with multiple projects and sections and sub-tasks

[Include templates](./template/include_template.md)

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

## License

See [license](../LICENSE)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/jamesbrond/todoist-template.svg?style=for-the-badge
[contributors-url]: https://github.com/jamesbrond/todoist-template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/jamesbrond/todoist-template.svg?style=for-the-badge
[forks-url]: https://github.com/jamesbrond/todoist-template/network/members
[stars-shield]: https://img.shields.io/github/stars/jamesbrond/todoist-template.svg?style=for-the-badge
[stars-url]: https://github.com/jamesbrond/todoist-template/stargazers
[issues-shield]: https://img.shields.io/github/issues/jamesbrond/todoist-template.svg?style=for-the-badge
[issues-url]: https://github.com/jamesbrond/todoist-template/issues
[license-shield]: https://img.shields.io/github/license/jamesbrond/todoist-template.svg?style=for-the-badge
[license-url]: https://github.com/jamesbrond/todoist-template/blob/master/LICENSE
