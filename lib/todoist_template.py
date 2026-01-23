"""Process a template file and create objects on Todoist"""
from abc import ABC, abstractmethod
from datetime import datetime
import os
import sys
import logging
import pickle
from typing import TextIO
from lib.config.config import TTOptions
from lib.i18n import _
from lib.todoist import TodoistTemplateAPI
from lib.template.template_factory import TemplateFactory, TodoistTemplateError


PROJECT_KEYS_LIST = ['color', 'is_favorite', 'view_style']
SECTION_KEYS_LIST = ['order']
TASK_KEYS_LIST = ['content', 'description', 'order', 'labels', 'priority',
                  'due_string', 'due_date', 'due_datetime', 'due_lang',
                  'assignee']


def copy_dict(source, filter_keys):
    """Copy only keys in filter_keys from source dict to a new dict"""
    return {key: value for key, value in source.items() if key in filter_keys}


class AbstractTodoistAction(ABC):
    """Abstract class to process a template file and create objects on Todoist"""

    def __init__(self, template: TTOptions):
        self._file: TextIO = None
        self._template_info: TTOptions = template
        self._quick_add: bool = False
        self._factory: TemplateFactory = None
        self._jobs: list = []

    @abstractmethod
    def run(self, api: TodoistTemplateAPI) -> int:
        """Process a template file and create objects on Todoist"""

    def factory(self) -> AbstractTodoistAction:
        """Create a TemplateFactory object"""

        if self._template_info.file == '-':
            self._factory = TemplateFactory(sys.stdin, self._template_info.type, skip_comments=not self._quick_add)
        elif self._template_info.file is not None:
            with open(self._template_info.file, "r", encoding="utf-8") as fd:
                self._factory = TemplateFactory(fd, self._template_info.type, skip_comments=not self._quick_add)

        return self

    def jobs(self) -> AbstractTodoistAction:
        """Generate jobs from template file"""

        if not self._factory:
            raise TodoistTemplateError("Factory is not initialized. Call factory() method first")

        if bool(self._template_info.variables) and isinstance(self._template_info.variables, list):
            self._jobs = [self._factory.render(var) for var in self._template_info.variables]
        else:
            self._jobs = [self._factory.render({})]

        return self


class QuickAddAction(AbstractTodoistAction):
    """Add a new item using the Quick Add implementation available in the official clients"""

    def __init__(self, template: TTOptions) -> None:
        super().__init__(template)
        self._quick_add = True
        self.factory()
        self.jobs()

    def run(self, api: TodoistTemplateAPI) -> int:
        """Add a new item using the Quick Add implementation available in the official clients"""
        logging.info("Quick add action")

        if not self._jobs:
            raise TodoistTemplateError("No jobs to process. Cannot upload None")

        for job in self._jobs:
            api.quick_add(job)

        return 0


class UndoAction(AbstractTodoistAction):
    """Rollback todoist-template actions"""

    def run(self, api: TodoistTemplateAPI) -> int:
        """Rollback todoist-template actions"""
        logging.info("Undo action")

        undo_filename = self._template_info.undo.file
        if self._template_info.dry_run:
            logging.info(_("dry run> Load rollback commands from %s"), undo_filename)
        else:
            logging.info(_("Load rollback commands from %s"), undo_filename)
        with open(undo_filename, "rb") as undo:
            api.rollback(pickle.load(undo))

        if not self._template_info.dry_run:
            logging.debug(_("Delete undo file %s"), undo_filename)
            os.remove(undo_filename)

        return 0


class TemplateAction(AbstractTodoistAction):
    """Process a template file and create objects on Todoist"""

    def __init__(self, template: TTOptions) -> None:
        super().__init__(template)
        self.factory()
        self.jobs()

    def run(self, api: TodoistTemplateAPI) -> int:
        """Create tasks in Todoist"""
        logging.info("Template action")

        template_filename = "".join([x if x.isalnum() else "" for x in self._template_info.file])

        if not self._jobs:
            raise TodoistTemplateError("No jobs to process. Cannot upload None")

        for job in self._jobs:
            logging.debug("processing job: %s", job)
            self._template(api, job)

        if not self._template_info.dry_run:
            now = datetime.now().strftime('%Y%m%d%H%M%S')
            undofolder = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), self._template_info.undo.folder)

            if not os.path.exists(undofolder):
                os.makedirs(undofolder)

            undofile = os.path.join(
                undofolder,
                f"{os.path.basename(template_filename)}-{now}.undo")

            self._store_rollback(api, undofile)

        return 0

    def _template(self, api: TodoistTemplateAPI, tpl_obj: any) -> None:
        for obj in tpl_obj:
            if isinstance(obj, str):
                # template with a single project root
                self._project(api, obj, tpl_obj[obj])
            elif isinstance(obj, list):
                for item in obj:
                    self._template(api, item)
            else:
                # template with multiple projects
                for prj in list(obj):
                    self._project(api, prj, obj[prj])

    def _project(self, api: TodoistTemplateAPI, name: str, content: dict) -> None:
        if name == 'tasks':
            # no project in template just Inbox tasks
            logging.debug("no project in template just Inbox tasks")
            for task in content:
                self._task(api, None, None, None, task)
        else:
            project = copy_dict(content, PROJECT_KEYS_LIST)
            project['name'] = name

            # create or modify project in Todoist
            project_id = api.project(project)

            for key, value in content.items():
                if key not in PROJECT_KEYS_LIST:
                    self._section(api, project_id, key, value)

    def _section(self, api: TodoistTemplateAPI, project_id: str, name: str, content: dict) -> None:
        if name == 'tasks':
            #  project with no section in template just tasks
            logging.debug("project with no section in template just tasks")
            for task in content:
                self._task(api, project_id, None, None, task)
        else:
            section = copy_dict(content, SECTION_KEYS_LIST)
            section['name'] = name
            section['project_id'] = project_id

            # create or modify section in Todoist
            section_id = api.section(section)

            for task in content.get('tasks', []):
                self._task(api, None, section_id, None, task)

    def _task(self,  # pylint: disable=too-many-positional-arguments
              api: TodoistTemplateAPI,
              project_id: str,
              section_id: str,
              parent_id: str,
              content: dict) -> None:
        task = copy_dict(content, TASK_KEYS_LIST)

        if parent_id is not None:
            task['parent_id'] = parent_id
        elif section_id is not None:
            task['section_id'] = section_id
        elif project_id is not None:
            task['project_id'] = project_id

        logging.debug("creating task: %s", task)
        # create or modify task in Todoist
        task_id = api.task(task, self._template_info.is_update_tasks)

        for subtask in content.get('tasks', []):
            self._task(api, None, None, task_id, subtask)

    def _store_rollback(self, api: TodoistTemplateAPI, filepath: str) -> None:
        """Save rollback instructions to filepath"""
        if api.undo_commands:
            logging.info(_("Save rollback commands to %s"), filepath)
            with open(filepath, "ab") as file:
                #  reverse a list array using slicing methods
                # command must be executed in reverse orders
                pickle.dump(api.undo_commands[::-1], file)
        else:
            logging.debug("no rollabck instructions to save")

# ~@:-]
