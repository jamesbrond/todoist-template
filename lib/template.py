import re
import json
import yaml
import logging
from lib.todoist import Todoist
from lib.CustomYamlLoader import CustomYamlLoader

class TodoistTemplate:
    """
    Import YAML template file into Todoist application
    """

    def __init__(self, api_token, is_test=False):
        self.api = Todoist(api_token, is_test)

    def parse(self, file, placelholders):
        """
        Parse the template YAML file using placeholdes dictionary
        """

        if file is None:
            return

        try:
            template = json.loads(file)
        except Exception:
            template = yaml.load(file, Loader=CustomYamlLoader)

        for t in template:
            if isinstance(t, str):
                # template with a single project root
                self._project(t, template[t], placelholders)
            else:
                # template with multiple projects
                p = list(t)[0]
                self._project(p, t[p], placelholders)

    def _parse_items(self, obj, list_keys, placeholders={}):
        item = {}
        for k in list_keys:
            if k in obj:
                item[k] = self._replace(obj[k], placeholders)
        return item

    def _replace(self, value, placeholders):
        result = re.search(r"\{([^|]+)\s*[|]?\s*(.*)\}", value)
        if not result:
            return value

        var = result.group(1)
        default = result.group(2)
        replace = placeholders.get(var)
        return str(replace) if replace else str(default)

    def _project(self, name, inner, placeholders):
        if name == "tasks":
            for task in inner:
                self._task(project_id=None, section_id=None, parent_id=None, task=task, placeholders=placeholders)
            return
        replaced_name = self._replace(name, placeholders)
        project_id = self.api.exists_project(replaced_name)
        is_new = False
        if not project_id:
            is_new = True
            project_id = self.api.add_project(replaced_name, self._parse_items(inner, ["color", "favorite"], placeholders))
        logging.info(f"Project: {self._isnew(is_new)}{replaced_name} ({project_id})")

        sections = list(inner)
        for section in sections:
            if section == "tasks":
                for task in inner[section]:
                    self._task(project_id=project_id, section_id=None, parent_id=None, task=task, placeholders=placeholders)
            else:
                logging.debug(f"{section}: {inner[section]}")
                self._section(project_id, section, inner[section], placeholders)

    def _section(self, project_id, name, content, placeholders):
        replaced_name = self._replace(name, placeholders)
        section_id = self.api.exists_section(replaced_name, project_id)

        is_new = False
        if not section_id:
            is_new = True
            section_id = self.api.add_section(replaced_name)
        logging.info(f"Section: {self._isnew(is_new)}{replaced_name} ({section_id})")

        if "tasks" in content:
            for task in content["tasks"]:
                self._task(project_id=None, section_id=section_id, parent_id=None, task=task, placeholders=placeholders)

    def _task(self, project_id, section_id, parent_id, task, placeholders):
        replaced_task = self._parse_items(task, ["content", "description", "completed", "priority", "due_string"], placeholders)

        if section_id is not None:
            replaced_task["section_id"] = section_id
        elif project_id is not None:
            replaced_task["project_id"] = project_id
        elif parent_id is not None:
            replaced_task["parent_id"] = parent_id

        if "labels" in task:
            label_ids = []
            for label in task["labels"]:
                label_ids.append(self._label(label, placeholders))
            replaced_task["label_ids"] = label_ids

        task_id = self.api.exists_task(project_id, section_id, replaced_task['content'])
        if task_id:
            is_new = False
            self.api.update_task(task_id, **replaced_task)
        else:
            is_new = True
            task_id = self.api.add_task(**replaced_task)
        logging.info(f"Task: {self._isnew(is_new)}{replaced_task['content']} ({task_id})")


        if "tasks" in task:
            for subtask in task["tasks"]:
                self._task(project_id=None, section_id=None, parent_id=task_id, task=subtask, placeholders=placeholders)
        return task_id

    def _label(self, name, placeholders):
        replaced_label = self._replace(name, placeholders)
        label_id = self.api.exists_label(replaced_label)
        is_new = False
        if not label_id:
            label_id = self.api.add_label(replaced_label)
            is_new = True
        logging.debug(f"Label: {self._isnew(is_new)} {replaced_label} ({label_id})")
        return label_id

    def _isnew(self, b):
        return '[NEW] ' if b else ''

# ~@:-]