"""Process a template file and create objects on Todoist"""
import logging
import pickle
from lib.i18n import _
from lib.todoist import Todoist
from lib.template.template_factory import TemplateFactory, TodoistTemplateError, TEMPLATE_TEXT


class TodoistTemplate:
    """Process a template file and create objects on Todoist"""

    PROJECT_KEYS_LIST = ['color', 'is_favorite', 'view_style']
    SECTION_KEYS_LIST = ['order']
    TASK_KEYS_LIST = ['content', 'description', 'order', 'labels', 'priority',
                      'due_string', 'due_date', 'due_datetime', 'due_lang',
                      'assignee']

    def __init__(self, api_token, dry_run=False, is_undo=False, is_quick_add=False):
        self.api_token = api_token
        self.todoist = Todoist(self.api_token, dry_run, is_undo, is_quick_add)
        self.update_task = False

    def _generate_jobs_list(self, file, file_type, variables=None):
        factory = TemplateFactory(file, file_type)
        if bool(variables):
            return [factory.render(vars) for vars in variables]
        return [factory.render({})]

    def template(self, template, update_task=False):
        """Create tasks in Todoist"""

        jobs = self._generate_jobs_list(template.file, template.type, template.variables)

        if not jobs:
            raise TodoistTemplateError("Cannot upload None")

        self.update_task = update_task

        for job in jobs:
            self._template(job)

    def store_rollback(self, filepath):
        """Save rollback instructions to filepath"""
        if self.todoist.undo_commands:
            logging.info(_("Save rollback commands to %s"), filepath)
            with open(filepath, "ab") as file:
                #  reverse a list array using slicing methods
                # command must be executed in reverse orders
                pickle.dump(self.todoist.undo_commands[::-1], file)
        else:
            logging.debug("no rollabck instructions to save")

    def rollback(self, file):
        """Load rollback instructions from file ad run rollback"""
        with file:
            logging.info(_("Load rollback commands from %s"), file.name)
            self.todoist.rollback(pickle.load(file))

    def quick_add(self, template):
        """Add a new item using the Quick Add implementation available in the official clients"""
        jobs = self._generate_jobs_list(template.file, TEMPLATE_TEXT, template.variables)

        if not jobs:
            raise TodoistTemplateError("Cannot upload None")

        for job in jobs:
            self.todoist.quick_add(job)

    def _template(self, tpl_obj):
        for obj in tpl_obj:
            if isinstance(obj, str):
                # template with a single project root
                self._project(obj, tpl_obj[obj])
            elif isinstance(obj, list):
                for item in obj:
                    self._template(item)
            else:
                # template with multiple projects
                for prj in list(obj):
                    self._project(prj, obj[prj])

    def _project(self, name, content):
        if name == 'tasks':
            # no project in template just Inbox tasks
            logging.debug("no project in template just Inbox tasks")
            for task in content:
                self._task(None, None, None, task)
            return

        project = self._copy_dict(content, self.PROJECT_KEYS_LIST)
        project['name'] = name

        # create or modify project in Todoist
        project_id = self.todoist.project(project)

        for key, value in content.items():
            if key not in self.PROJECT_KEYS_LIST:
                self._section(project_id, key, value)

    def _section(self, project_id, name, content):
        if name == 'tasks':
            #  project with no section in template just tasks
            logging.debug("project with no section in template just tasks")
            for task in content:
                self._task(project_id, None, None, task)
            return

        section = self._copy_dict(content, self.SECTION_KEYS_LIST)
        section['name'] = name
        section['project_id'] = project_id

        # create or modify section in Todoist
        section_id = self.todoist.section(section)

        for task in content.get('tasks', []):
            self._task(None, section_id, None, task)

    def _task(self, project_id, section_id, parent_id, content):
        task = self._copy_dict(content, self.TASK_KEYS_LIST)

        if parent_id is not None:
            task['parent_id'] = parent_id
        elif section_id is not None:
            task['section_id'] = section_id
        elif project_id is not None:
            task['project_id'] = project_id

        # create or modify task in Todoist
        task_id = self.todoist.task(task, self.update_task)

        for subtask in content.get('tasks', []):
            self._task(None, None, task_id, subtask)

    def _copy_dict(self, source, filter_keys):
        return {key: value for key, value in source.items() if key in filter_keys}

# ~@:-]
