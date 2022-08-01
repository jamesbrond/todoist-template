import logging
import lib.utils as utils
from todoist_api_python.api import TodoistAPI

class Todoist():
    def __init__(self, api_token, is_test=False):
        self.api = TodoistAPI(api_token)
        self.projects = self.get_projects()
        self.sections = self.get_sections()
        self.labels = self.get_labels()
        self.is_test = is_test

    def get_labels(self):
        return self.api.get_labels()

    def get_projects(self):
        return self.api.get_projects()

    def get_sections(self):
        return self.api.get_sections()

    def exists_project(self, name):
        """Returns the Todoist project ID if project exists; False otherwise"""
        return self._exists(name, self.projects)

    def exists_section(self, name, project_id):
        """Returns the Todoist section ID if section exists; False otherwise"""
        _id = utils.find_needle_in_haystack([name, project_id], self.sections, ["name", "project_id"])
        return _id if _id is not None else False

    def exists_label(self, name):
        """Returns the Todoist label ID if label exists; False otherwise"""
        return self._exists(name, self.labels)

    def exists_task(self, project_id, section_id, content):
        """Returns the Todoist task ID if task exists in the given project or section; False otherwise """
        if not project_id and not section_id:
            return False
        query = {
            'project_id': project_id,
            'section_id': section_id
        }
        tasks = self.api.get_tasks(**query)
        return self._exists(content, tasks, ["content"])

    def add_project(self, name, **kwargs):
        """Creates a new project and returns its ID """
        if self.is_test:
            return None
        project = self.api.add_project(name=name, **kwargs)
        self.projects.append(project)
        logging.debug(f"created new project: {str(project)}")
        return project.id

    def add_section(self, name, **kwargs):
        """Creates a new section and returns its ID """
        if self.is_test:
            return None
        section = self.api.add_section(name=name, **kwargs)
        self.sections.append(section)
        logging.debug(f"created new section: {str(section)}")
        return section.id

    def add_label(self, name, **kwargs):
        if self.is_test:
            return None
        label = self.api.add_label(name=name, **kwargs)
        self.labels.append(label)
        logging.debug(f"created new label: {str(label)}")
        return label.id

    def add_task(self, content: str, **kwargs):
        if self.is_test:
            return None
        task = self.api.add_task(content, **kwargs)
        logging.debug(f"created new task: {str(task)}")
        return task.id

    def update_task(self, task_id:int, **kwargs):
        if not self.is_test:
            self.api.update_task(task_id=task_id, **kwargs)
            logging.debug(f"update task: {task_id}")
        return True

    def _exists(self, needle, haystack, params=[ "name" ]):
        _id = utils.find_needle_in_haystack([needle], haystack, params)
        return _id if _id is not None else False

# ~@:-]