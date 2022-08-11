# The template YAML syntax

## Project

**name** [String]

Name of the project.

**color** [Integer]

Optional. A numeric ID representing the color of the project icon. Refer to the ID column in the [Colors](https://developer.todoist.com/guides/#colors) guide for more info.

**favorite** [Boolean]

Optional. Whether the project is a favorite (a true or false value).

```yaml
New Project:
  color: 40
  favorite: true
  tasks:
    - content: delete me
      priority: 3
      due_string: tod
```

## Section

**name** [String]

Section name.

**order** [Integer]

Optional. Order among other sections in the project.

```yaml
New Project:
  New Section:
    order: 1
    tasks:
      - content: delete me
        priority: 3
        due_string: tod
```

## Task

**content** [String]

Task content. This value may contain markdown-formatted text and hyperlinks. Details on Markdown support can be found in the [Text Formatting article](https://todoist.com/help/articles/text-formatting) in the Todoist Help Center.

**description** [String]

A description for the task. This value may contain markdown-formatted text and hyperlinks. Details on Markdown support can be found in the [Text Formatting article](https://todoist.com/help/articles/text-formatting) in the Todoist Help Center.

**labels** [Array of String]

Array of label name, associated with a task. If the label do not exist in Todoist it will be created. They can be define as list of items

```yaml
  labels:
    - "label 0"
    - "label 1"
```

or as array:

```yaml
labels: [ "label 0", "label 1" ]
```

**priority** [Integer]

Task priority from 1 (normal, default value) to 4 (urgent).

**due_string** [String]

Human defined date in arbitrary format. See [some example date formats you can use](https://todoist.com/help/articles/due-dates-and-times).

**due_date** [String]

Specific date in YYYY-MM-DD format relative to user’s timezone.

**due_datetime** [String]

Specific date and time in RFC3339 format in UTC.

**due_lang** [String]

2-letter code specifying language in case due_string is not written in English.

**order** [Integer]

Non-zero integer value used by clients to sort tasks under the same parent.
