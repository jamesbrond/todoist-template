# Parameterized template

todoist-template allows you to write templates, using variables like this:

```yaml
# param_template_0.yml
Personal:
  Fitness:
    tasks:
      -
        content: Tabata
        due_string: {day1}
      -
        content: Resistance
        due_string: {day2}
      -
        content: Treadmill
        due_string: {day3}
```

We use the same [Three simple tasks](./simple_template.md#three-simple-tasks) example, but here we use variables for the due dates.
When this template is rendered, using the `-D day1=sun, day2=tue, day3=fri` paramenters:

```shell
python todoist-template.py param_template_0.yml -D day1=sun, day2=tue, day3=fri
```

the result is the same as running:

```yaml
Personal:
  Fitness:
    tasks:
      -
        content: Tabata
        due_string: sun
      -
        content: Resistance
        due_string: tue
      -
        content: Treadmill
        due_string: fri
```

## Where use variables

Variables can be used everywhere: project, session or task name, label, due date string, priority and description.

Morehover you can use variables to replace only part of a string. For example:

```yaml
tasks:
    -
    content: My task
    due_string: every {dayofweek}
```

Run with argument `-D dayofweek=Monday` to have a recursive task every Monday.

## Default values

You can specify a default value that will be used when the command-line value is not provided.

In order to set a default value use the pipe (`|`) characther after variable name:

```yaml
{variable|default value}
```

For example:

```yaml
# param_template_3.yml
"{prj|Inbox}":
    tasks:
      - content: Task1
        due_string: "{day | tod}"
      - content: Task2
        due_string: "{day|tomorrow}"
```

In this example if you do not use `-D prj=<some project name>` the default `Inbox` will be used. The same for due date of `Task1` and `Task2` it will be set to today and tomorrow, respectively if `-D day=<some day>` it's not used.

Prev [Simple template](./simple_template.md)
Next [Complex template](./complex_template.md)
