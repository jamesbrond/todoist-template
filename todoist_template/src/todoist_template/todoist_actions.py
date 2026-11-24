"""Process a template file and create objects on Todoist"""
from dataclasses import dataclass, field
import json
import logging
from pathlib import Path
from typing import Any
from todoist_template.template.template_factory import TTemplate
from todoist_template.template.template_factory import TemplateFactory
from todoist_template.todoist_api_wrapper import TodoistAPIWrapper
from todoist_template.utils import copy_dict
from todoist_template.i18n import _t


PROJECT_KEYS_LIST = ['color', 'is_favorite', 'view_style']
SECTION_KEYS_LIST = ['order']
TASK_KEYS_LIST = ['content', 'description', 'order', 'labels', 'priority',
                  'due_string', 'due_date', 'due_datetime', 'due_lang',
                  'assignee']


@dataclass
class TemplateContext:
    """Template context dataclass"""
    api: TodoistAPIWrapper
    template: TTemplate
    variables: list[dict] = field(default_factory=list[dict])
    is_update_tasks: bool = False
    is_dry_run: bool = False


class TodoistTemplateError(Exception):
    """Todoist-Template exception"""
    pass

def jobs_factory(template: TTemplate, variables: list[dict] | None, quick_add: bool = False) -> list[dict]:
    """Create a list of jobs from template and variables"""
    logging.debug("Creating jobs from template: %s with variables: %s", template, variables)
    factory = TemplateFactory(template, keep_comments=quick_add)
    if variables:
        return [factory.render(var) for var in variables]
    return [factory.render({})]


def quick_add_action(context: TemplateContext) -> int:
    """Quick add tasks to Todoist"""
    logging.info(_t("Quick add action"))
    jobs = jobs_factory(context.template, context.variables, quick_add=True)

    if len(jobs) == 0:
        logging.error("No jobs to process. Cannot upload None")
        raise TodoistTemplateError("No jobs to process. Cannot upload None")

    logging.debug("jobs to process: %i", len(jobs))
    for job in jobs:
        logging.debug("processing job: %s", job)
        context.api.quick_add(job)
    return len(jobs)


def undo_action(context: TemplateContext) -> int:
    """Rollback todoist-template actions"""
    logging.info(_t("Undo action"))

    undo_filepath: Path = context.template.undo_file
    if context.is_dry_run:
        logging.info(_t("dry run>") + ' ' + _t("Load rollback commands from %s") % undo_filepath)
    else:
        logging.info(_t("Load rollback commands from %s") % undo_filepath)
    with open(undo_filepath, "r", encoding="utf-8") as undo:
        context.api.rollback(json.load(undo), is_dry_run=context.is_dry_run)

    if not context.is_dry_run:
        logging.debug("delete undo file %s", undo_filepath)
        undo_filepath.unlink()

    return 1


def template_action(context: TemplateContext) -> int:
    """Create tasks in Todoist"""
    logging.info(_t("Template action"))

    jobs = jobs_factory(context.template, context.variables, quick_add=False)
    if not jobs:
        raise TodoistTemplateError("No jobs to process. Cannot upload None")

    logging.debug("jobs to process: %i", len(jobs))
    for job in jobs:
        logging.debug("processing job: %s", job)
        _template(context.api, job, context.is_update_tasks)

    if not context.is_dry_run:
        _store_rollback(context.api, context.template.undo_file_from_template)

    return len(jobs)


def _template(api: TodoistAPIWrapper, tpl_obj: Any, is_update_tasks: bool) -> None:
    for obj in tpl_obj:
        if isinstance(obj, str):
            # template with a single project root
            _project(api, obj, tpl_obj[obj], is_update_tasks)
        elif isinstance(obj, list):
            for item in obj:
                _template(api, item, is_update_tasks)
        else:
            # template with multiple projects
            for prj in list(obj):
                _project(api, prj, obj[prj], is_update_tasks)


def _project(api: TodoistAPIWrapper, name: str, content: dict, is_update_tasks: bool) -> None:
    if name == 'tasks':
        # no project in template just Inbox tasks
        logging.debug("no project in template just Inbox tasks")
        for task in content:
            _task(api, None, None, None, task, is_update_tasks)
    else:
        project = copy_dict(content, PROJECT_KEYS_LIST)
        project['name'] = name

        # create or modify project in Todoist
        project_id = api.project(project)

        for key, value in content.items():
            if key not in PROJECT_KEYS_LIST:
                _section(api, project_id, key, value, is_update_tasks)


def _section(api: TodoistAPIWrapper, project_id: str, name: str, content: dict, is_update_tasks: bool) -> None:
    if name == 'tasks':
        #  project with no section in template just tasks
        logging.debug("project with no section in template just tasks")
        for task in content:
            _task(api, project_id, None, None, task, is_update_tasks)
    else:
        section = copy_dict(content, SECTION_KEYS_LIST)
        section['name'] = name
        section['project_id'] = project_id

        # create or modify section in Todoist
        section_id = api.section(section)

        for task in content.get('tasks', []):
            _task(api, None, section_id, None, task, is_update_tasks)


def _task(api: TodoistAPIWrapper,  # pylint: disable=too-many-positional-arguments
          project_id: str,
          section_id: str,
          parent_id: str,
          content: dict,
          is_update_tasks: bool) -> None:
    task = copy_dict(content, TASK_KEYS_LIST)

    if parent_id is not None:
        task['parent_id'] = parent_id
    elif section_id is not None:
        task['section_id'] = section_id
    elif project_id is not None:
        task['project_id'] = project_id

    logging.debug("creating task: %s", task)
    # create or modify task in Todoist
    task_id = api.task(task, is_update_tasks)

    for subtask in content.get('tasks', []):
        _task(api, None, None, task_id, subtask, is_update_tasks)


def _store_rollback(api: TodoistAPIWrapper, filepath: Path) -> None:
    """Save rollback instructions to filepath"""
    if api._undo_commands:
        logging.info(_t("Save rollback commands to %s"), filepath)
        json_undo_command = json.dumps(api._undo_commands[::-1], indent=0, ensure_ascii=False)
        with filepath.open("w", encoding="utf-8") as file:
            file.write(json_undo_command)
    else:
        logging.debug("no rollback instructions to save")

# ~@:-]
