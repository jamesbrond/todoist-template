# The template YAML syntax

## Task

**content** [String]

Task content. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://todoist.com/help/articles/text-formatting) in the Todoist Help Center.

**description** [String]

A description for the task. This value may contain markdown-formatted text and hyperlinks. Details on markdown support can be found in the [Text Formatting article](https://todoist.com/help/articles/text-formatting) in the Todoist Help Center.

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

**priority** (Integer)

Task priority from 1 (normal, default value) to 4 (urgent).

**due_string** (String)

Human defined date in arbitrary format. See [some example date formats you can use](https://todoist.com/help/articles/due-dates-and-times).
