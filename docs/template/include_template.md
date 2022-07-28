# Inlcude templates

Divide et impera (divide and rule), or break up a complex template into pieces that are more easy to maintaine.

In todoist-template you can include templates inside another with the custom `!include <filename>` handler.
This feature **is not supported in JSON template** files.

```yaml
# include_template_0.yml
- Personal:
  tasks:
      -
        content: Stay focused and motivated
        due_string: every day

- !include param_template_0.yml
- !include param_template_1.yml
- !include param_template_2.yml
```

**NB**: All the template share the same variables.

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

```yaml
# param_template_1.yml
Personal:
  Diet:
    tasks:
      -
        content: Protein dinner
        due_string: "{day1} 19:30"
        priority: 2
      -
        content: Protein dinner
        due_string: "{day2} 19:30"
        priority: 2
      -
        content: Protein dinner
        due_string: "{day3} 19:30"
        priority: 2
```

```yaml
# param_template_2.yml
Home:
  Shopping List:
    tasks:
      -
        content: Buy meat for three dinners
        due_string: "{day1} morning"
        labels: [ "butcher shop"]
        priority: 2
```
