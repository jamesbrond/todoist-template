"""Tansform a template into Todoist tasks"""

import logging
import re
from lib.todoist import Todoist
from lib.loader.loaderfactory import TemplateLoaderFactory
from lib.i18n import _


PLACEHOLDER_REGEXP = re.compile(r"{(\w+)\s*\|?\s*([^}]+)?}")


class TodoistTemplate:
    """
    Import YAML template file into Todoist application
    """

    def __init__(self, api_token, dry_run=False, is_update=False):
        self.todoist = Todoist(api_token, dry_run, is_update)
        self.placeholders = {}
        self.template = None
        self.is_update = is_update

    def parse(self, file, placeholders, undofile=None):
        """
        Parse the template YAML file using placeholdes dictionary
        """

        self.placeholders = placeholders or {}
        logging.debug(_("Placeholders: %s"), str(self.placeholders))

        if file is None and self.template is None:
            return

        if self.template is None:
            template_loader = TemplateLoaderFactory().get_loader(file.name)
            logging.debug(_("use %s to load '%s' file"), template_loader.__class__.__name__, file.name)

            self.template = template_loader.load(file)

        if self.template:
            try:
                for templ in self.template:
                    if isinstance(templ, str):
                        # template with a single project root
                        self._project(templ, self.template[templ])
                    else:
                        # template with multiple projects
                        prj = list(templ)[0]
                        self._project(prj, templ[prj])
            except:
                logging.error(_("Something went wrong: undo all changes"))
                self.todoist.rollback()
                # re-throw exception to main
                raise

            if undofile:
                self.todoist.store_rollback(undofile)
        else:
            logging.error(_("No template defined"))

    def rollback(self, file):
        """Applies rollback actions in file"""
        self.todoist.load_rollback(file)
        return self.todoist.rollback()

    def _filter_and_replace(self, obj, list_keys):
        return {k: self._replace(obj[k]) for k in list_keys if k in obj}

    def _replace(self, value):
        if not isinstance(value, str):
            # {placholder} are always strings
            return value
        return PLACEHOLDER_REGEXP.sub(
            lambda x: self.placeholders.get(x.group(1)) or x.group(2),
            value
        )

    def _project(self, name, inner):
        if name == "tasks":
            for task in inner:
                self._task(
                    project_id=None,
                    section_id=None,
                    parent_id=None,
                    task=task
                )
            return
        replaced_name = self._replace(name)
        project_id = self.todoist.exists_project(replaced_name)
        is_new = False
        if not project_id:
            is_new = True
            project_id = self.todoist.new_project(
                replaced_name,
                args=self._filter_and_replace(inner, ["color", "favorite"])
            )
        logging.info(_("Project: %s%s (%s)"), self._isnew(is_new), replaced_name, project_id)

        sections = list(inner)
        for section in sections:
            if section == "tasks":
                for task in inner[section]:
                    self._task(
                        project_id=project_id,
                        section_id=None,
                        parent_id=None,
                        task=task
                    )
            elif isinstance(inner[section], dict):
                # if it'a a dict it'a section becouse we exclude tasks in the previous if
                self._section(project_id, section, inner[section])

    def _section(self, project_id, name, content):
        replaced_name = self._replace(name)
        section_id = self.todoist.exists_section(replaced_name, project_id)

        is_new = False
        if not section_id:
            is_new = True
            section_id = self.todoist.new_section(
                replaced_name,
                args=self._filter_and_replace(content, ["order"])
            )
        logging.info(_("Section: %s%s (%s)"), self._isnew(is_new), replaced_name, section_id)

        if "tasks" in content:
            for task in content["tasks"]:
                self._task(
                    project_id=None,
                    section_id=section_id,
                    parent_id=None,
                    task=task
                )

    def _task(self, project_id, section_id, parent_id, task):
        replaced_task = self._filter_and_replace(
            task,
            ["content", "description", "completed", "priority",
             "due_string", "due_date", "due_datetime", "due_lang", "order"]
        )

        if section_id is not None:
            replaced_task["section_id"] = section_id
        elif project_id is not None:
            replaced_task["project_id"] = project_id
        elif parent_id is not None:
            replaced_task["parent_id"] = parent_id

        if "labels" in task:
            label_ids = []
            for label in task["labels"]:
                label_ids.append(self._label(label))
            replaced_task["label_ids"] = label_ids

        if self.is_update:
            task_id = self.todoist.exists_task(project_id, section_id, replaced_task["content"])
        else:
            task_id = None
        if task_id:
            logging.debug(_("task already exists"))
            is_new = False
            self.todoist.modify_task(task_id, **replaced_task)
        else:
            logging.debug(_("task doesn't exist yet"))
            is_new = True
            task_id = self.todoist.new_task(**replaced_task)
        logging.info(_("Task: %s%s (%s)"), self._isnew(is_new), replaced_task['content'], task_id)

        if "tasks" in task:
            for subtask in task["tasks"]:
                self._task(
                    project_id=None,
                    section_id=None,
                    parent_id=task_id,
                    task=subtask
                )
        return task_id

    def _label(self, name):
        replaced_name = self._replace(name)
        label_id = self.todoist.exists_label(replaced_name)
        is_new = False
        if not label_id:
            label_id = self.todoist.new_label(replaced_name)
            is_new = True
        logging.debug(_("Label: %s%s (%s)"), self._isnew(is_new), replaced_name, label_id)
        return label_id

    def _isnew(self, is_new):
        return "[NEW] " if is_new else ""


# ~@:-]
