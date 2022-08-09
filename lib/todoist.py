"""Layer module to handle Todoist API"""

import logging
import pickle
import json
import requests
from todoist_api_python.api import TodoistAPI
import lib.utils as utils


SYNC_API = "https://api.todoist.com/sync/v9/sync"

class Todoist(TodoistAPI):
    """Layer class to handle Todoist API"""
    def __init__(self, api_token: str, dry_run=False, session=None):
        super().__init__(api_token, session)
        self.projects = self.get_projects()
        self.sections = self.get_sections()
        self.labels = self.get_labels()
        self.dry_run = dry_run
        self.undo_commands = []

    def exists_project(self, name):
        """Returns the Todoist project ID if project exists; False otherwise"""
        return self._exists([name], self.projects, ["name"])

    def exists_section(self, name, project_id):
        """Returns the Todoist section ID if section exists; False otherwise"""
        return self._exists([name, project_id], self.sections, ["name", "project_id"])

    def exists_label(self, name):
        """Returns the Todoist label ID if label exists; False otherwise"""
        return self._exists([name], self.labels, ["name"])

    def exists_task(self, project_id, section_id, content):
        """Returns the Todoist task ID if task exists
        in the given project or section; False otherwise"""
        if not project_id and not section_id:
            return False
        query = {"project_id": project_id, "section_id": section_id}
        tasks = self.get_tasks(**query)
        return self._exists([content], tasks, ["content"])

    def new_project(self, name, **kwargs):
        """Creates a new project and returns its ID"""
        if self.dry_run:
            return None
        project = self.add_project(name=name, **kwargs)
        self.projects.append(project)
        logging.debug("created new project: %s", project)
        self.undo_commands.append(self._add_undo_command("project_delete", project.id))
        return project.id

    def new_section(self, name, **kwargs):
        """Creates a new section and returns its ID"""
        if self.dry_run:
            return None
        section = self.add_section(name=name, **kwargs)
        self.sections.append(section)
        logging.debug("created new section: %s", section)
        self.undo_commands.append(self._add_undo_command("section_delete", section.id))
        return section.id

    def new_label(self, name, **kwargs):
        """Adds new label"""
        if self.dry_run:
            return None
        label = self.add_label(name=name, **kwargs)
        self.labels.append(label)
        logging.debug("created new label: %s", label)
        self.undo_commands.append(self._add_undo_command("label_delete", label.id))
        return label.id

    def new_task(self, content: str, **kwargs):
        """Adds new task"""
        if self.dry_run:
            return None
        task = self.add_task(content, **kwargs)
        logging.debug("created new task: %s", task)
        self.undo_commands.append(self._add_undo_command("item_delete", task.id))
        return task.id

    def modify_task(self, task_id: int, **kwargs):
        """Modifies existing task"""
        if not self.dry_run:
            original_task =  self.get_task(task_id=task_id).to_dict()
            if self.update_task(task_id=task_id, **kwargs):
                logging.debug("update task: %d", task_id)
                self.undo_commands.append(
                    self._add_undo_command("item_update", task_id, {
                        "id": task_id,
                        "content": original_task["content"],
                        "description": original_task["description"],
                        "due": original_task["due"],
                        "priority": original_task["priority"],
                        "labels": original_task["label_ids"],
                        "assigned_by_uid": original_task["assigner"],
                        "responsible_uid": original_task["assignee"],
                        "day_order": original_task["order"]
                    })
                )
        return True

    def store_rollback(self, filepath):
        """Save rollback instructions to filepath"""
        logging.info("Save rollback commands to %s", filepath)
        with open(filepath, "wb") as file:
            pickle.dump(self.undo_commands, file)

    def load_rollback(self, file):
        """Load rollback instructions from file"""
        logging.info("Load rollback commands from %s", file.name)
        self.undo_commands = pickle.load(file)

    def rollback(self, undo_commands=None):
        """Rollback todoist-template actions"""
        cmds = undo_commands if undo_commands else self.undo_commands
        status = self._do_rollback(cmds)
        logging.info("Rollback status: %s", ("Success" if status else "Failure"))
        return status

    def _do_rollback(self, commands):
        logging.debug("undo commands: %s", commands)
        response = self._sync(commands)
        logging.debug("undo response %s", response)
        if response and response.get("sync_status"):
            for _, sync_message in response.get("sync_status").items():
                if sync_message != "ok":
                    return False
            return True
        return False

    def _sync(self, commands=None):
        if not commands:
            params = {
                "sync_token": "*",
                "resource_types": '["all"]'
            }
        else:
            params = {"commands": json.dumps(commands, skipkeys=True, allow_nan=False)}

        response = requests.get(SYNC_API,
            headers={"Authorization": f"Bearer {self._token}"},
            params=params
        )
        return response.json() if response.status_code == 200 else response.content

    def _exists(self, needle, haystack, params):
        _item = utils.find_needle_in_haystack(needle, haystack, params)
        if _item:
            return getattr(_item, "id")
        return False

    def _add_undo_command(self, cmd_type, obj_id, args=None):
        cmd = {
            "type": cmd_type,
            "uuid": utils.uid(),
            "args": {
                "id": obj_id
            }
        }

        if args:
            for key in args:
                cmd["args"][key] = args[key]

        return cmd

# ~@:-]
