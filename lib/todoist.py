"""Layer module to handle Todoist API"""

import logging
import pickle
import json
import requests
from todoist_api_python.api import TodoistAPI
from lib.utils import find_needle_in_haystack, uid
from lib.i18n import _


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
        logging.debug(_("get tasks for %s"), query)
        tasks = self.get_tasks(**query)
        logging.debug(_("found %d tasks"), len(tasks))
        return self._exists([content], tasks, ["content"])

    def new_project(self, name, args):
        """Creates a new project and returns its ID"""
        if self.dry_run:
            logging.debug(_("created new project: %s: %s"), name, args)
            return None
        project = self.add_project(name=name, **args)
        self.projects.append(project)
        logging.debug(_("created new project: %s"), project)
        self.undo_commands.append(self._add_undo_command("project_delete", project.id))
        return project.id

    def new_section(self, name, args):
        """Creates a new section and returns its ID"""
        if self.dry_run:
            logging.debug(_("created new section: %s: %s"), name, args)
            return None
        section = self.add_section(name=name, **args)
        self.sections.append(section)
        logging.debug(_("created new section: %s"), section)
        self.undo_commands.append(self._add_undo_command("section_delete", section.id))
        return section.id

    def new_label(self, name, **kwargs):
        """Adds new label"""
        if self.dry_run:
            return None
        label = self.add_label(name=name, **kwargs)
        self.labels.append(label)
        logging.debug(_("created new label: %s"), label)
        self.undo_commands.append(self._add_undo_command("label_delete", label.id))
        return label.id

    def new_task(self, **kwargs):
        """Adds new task"""
        if self.dry_run:
            return None
        task = self.add_task(**kwargs)
        logging.debug(_("created new task: %s"), task)
        self.undo_commands.append(self._add_undo_command("item_delete", task.id))
        return task.id

    def modify_task(self, task_id: int, **kwargs):
        """Modifies existing task"""
        if not self.dry_run:
            original_task = self.get_task(task_id=task_id).to_dict()
            if self.update_task(task_id=task_id, **kwargs):
                logging.debug(_("update task: %s"), str(task_id))
                self.undo_commands.append(
                    self._add_undo_command("item_update", task_id, {
                        "id": task_id,
                        "content": original_task["content"],
                        "description": original_task["description"],
                        "due": original_task["due"],
                        "priority": original_task["priority"],
                        "labels": original_task["labels"],
                        "assigned_by_uid": original_task["assigner_id"],
                        "responsible_uid": original_task["assignee_id"],
                        "day_order": original_task["order"]
                    })
                )
        return True

    def store_rollback(self, filepath):
        """Save rollback instructions to filepath"""
        logging.debug(_("Save rollback commands to %s"), filepath)
        with open(filepath, "ab") as file:
            pickle.dump(self.undo_commands, file)

    def load_rollback(self, file):
        """Load rollback instructions from file"""
        logging.info(_("Load rollback commands from %s"), file.name)
        self.undo_commands = pickle.load(file)

    def rollback(self, undo_commands=None):
        """Rollback todoist-template actions"""
        cmds = undo_commands if undo_commands else self.undo_commands
        status = self._do_rollback(cmds)
        logging.info(_("Rollback status: %s"), (_("Success") if status else _("Failure")))
        return status

    def _do_rollback(self, commands):
        logging.debug(_("undo commands: %s"), commands)
        response = self._sync(commands)
        logging.debug(_("undo response %s"), response)
        if response and response.get("sync_status"):
            for k, sync_message in response.get("sync_status").items():  # pylint: disable=unused-variable
                if sync_message != "ok":
                    return False
            return True
        return False

    def _sync(self, commands=None):
        if commands is None:
            params = {
                "sync_token": "*",
                "resource_types": '["all"]'
            }
        else:
            params = {"commands": json.dumps(commands, skipkeys=True, allow_nan=False)}

        response = requests.get(
            SYNC_API,
            headers={"Authorization": f"Bearer {self._token}"},
            params=params,
            timeout=60.0
        )
        return response.json() if response.status_code == 200 else response.content

    def _exists(self, needle, haystack, params):
        _item = find_needle_in_haystack(needle, haystack, params)
        if _item:
            return getattr(_item, "id")
        return False

    def _add_undo_command(self, cmd_type, obj_id, args=None):
        cmd = {
            "type": cmd_type,
            "uuid": uid(),
            "args": {
                "id": obj_id
            }
        }

        if args:
            for key in args:
                cmd["args"][key] = args[key]

        return cmd

# ~@:-]
