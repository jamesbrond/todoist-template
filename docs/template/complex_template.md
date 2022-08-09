# Complex template

Until now we have seen how to create one or more tasks related to a project or session. Now let's see something more complex:

```yaml
# complex_template_0.yml
- Personal:
  tasks:
      -
        content: Stay focused and motivated
        due_string: every day
  Fitness:
    tasks:
      -
        content: Tabata
        due_string: mon
      -
        content: Resistance
        due_string: wed
      -
        content: Treadmill
        due_string: fri
  Diet:
    tasks:
      -
        content: Protein dinner
        due_string: every two day at 19:30 from mon until fri
        priority: 2

- Home:
    Shopping List:
      tasks:
        -
          content: Buy meat for three dinners
          due_string: mon morning
          labels: [ "butcher shop"]
          priority: 2
```

In this example we create a lot of tasks in two projects, but let's see in details.

```yaml
- Personal:
    tasks:
        -
          content: Stay focused and motivated
          due_string: every day
```

This piece create one task directly attached to the *"Personal"* project.

```yaml
    Fitness:
      tasks:
        -
          content: Tabata
          due_string: mon
        -
          content: Resistance
          due_string: wed
        -
          content: Treadmill
          due_string: fri
    Diet:
      tasks:
        -
          content: Protein dinner
          due_string: every two day at 19:30 from mon until fri
          priority: 2
```

Here we use two sections of the *"Personal"* project to append tasks.

```yaml
- Home:
    Shopping List:
      tasks:
        -
          content: Buy meat for three dinners
          due_string: mon morning
          labels: [ "butcher shop"]
          priority: 2
```

Finally we add new task in another project under *"Home /Shopping List*.

## Sub-Task

In Todoist, you can easily break big, overwhelming tasks into small, manageable sub-tasks (and break down those sub-tasks into even smaller ones if you like).

In `todoist-template` you do this adding a `tasks` array to a task.

```yaml
# complex_template_1.yml
Fitness:
  tasks:
    - content: Tabata
      due_string: mon
      tasks:
        - content: High knees
          description: Warm up with 8 rounds of high knees - 20 seconds of work followed by 10 seconds of rest
        - content: 60-second recovery
        - content: Squats or lunges
          description: 8 rounds of your chosen leg exercise - 20 seconds of work followed by 10 seconds of rest
        - content: 60-second recovery
        - content: Crunches
          description: 8 rounds of crunches - 20 seconds of work followed by 10 seconds of rest
    - content: Resistance
      due_string: wed
    - content: Treadmill
      due_string: fri
```

There is no limit to what sub-sub-sub tasks you can add. However, having too deep task nesting is not always an advantage from a functional point of view and goes a bit against the philosophy of Todoist.

Prev [Parameterized template](./param_template.md)
Next [Inlcude templates](./include_template.md)
