"""Layer module to handle Todoist API"""

import logging
import json
import requests
from todoist_api_python.api import TodoistAPI
from lib.template import TodoistTemplateError
from lib.utils import find_needle_in_haystack, uid
from lib.i18n import _


class Todoist(TodoistAPI):
    """Layer class to handle Todoist API"""

    SYNC_API = "https://api.todoist.com/sync/v9"

    def __init__(self, api_token, dry_run=False, is_undo=False):
        super().__init__(api_token, None)
        self.dry_run = dry_run
        self.undo_commands = []
        if not is_undo:
            try:
                self.projects = self.get_projects()
                logging.debug('retrieved %d project from Todoist', len(self.projects))
                self.sections = self.get_sections()
                logging.debug('retrieved %d sections from Todoist', len(self.sections))
                self.collaborators = []
            except:
                self._session.close()
                raise

    def close(self):
        """Close all connections to Todoist"""
        self._session.close()

    def project(self, project):
        """
        Create a new project unless a project with the same name already exists.
        In any case it returns the project ID
        """
        project_id = self._exists_project(project['name'])
        if project_id:
            logging.info(self._log_message(_('Project'), project['name'], project_id, False))
            self.collaborators = self.get_collaborators(project_id)
            return project_id

        logging.info(self._log_message(_('Project'), project['name']))
        if self.dry_run:
            return None
        new_project = self.add_project(**project)
        self.projects.append(new_project)
        self.undo_commands.append(self._add_undo_command("project_delete", new_project.id))
        return new_project.id

    def section(self, section):
        """
        Create a new section unless a section with the same name in the same project
        already exists. In any case it returns the section ID
        """
        section_id = self._exists_section(section['name'], section['project_id'])
        if section_id:
            logging.info(self._log_message(_('Section'), section['name'], section_id, False))
            return section_id

        logging.info(self._log_message(_('Section'), section['name']))
        if self.dry_run:
            return None
        new_section = self.add_section(**section)
        self.sections.append(new_section)
        self.undo_commands.append(self._add_undo_command("section_delete", new_section.id))
        return new_section.id

    def task(self, task, update=False):
        """Create or update task"""
        if task.get('assignee'):
            task['assignee_id'] = self.get_collaborator_id(task.get('assignee'))

        if update:
            task_id = self._exists_task(
                task.get('project_id'),
                task.get('section_id'),
                task.get('content'))
        else:
            task_id = None

        if self.dry_run:
            logging.info(self._log_message(_('Task'), task['content'], task_id, task_id is None))
            return None

        if task_id:
            is_new = False
            original_task = self.get_task(task_id=task_id).to_dict()
            if self.update_task(task_id=task_id, **task):
                logging.debug(_("update task: %s"), str(task_id))
                self.undo_commands.append(self._add_undo_command("item_update", task_id, original_task))
        else:
            is_new = True
            new_task = self.add_task(**task)
            logging.debug(_("created new task: %s"), task)
            self.undo_commands.append(self._add_undo_command("item_delete", new_task.id))
            task_id = new_task.id

        logging.info(self._log_message(_('Task'), task['content'], task_id, is_new))
        return task_id

    def _exists_project(self, name):
        """Returns the Todoist project ID if project exists; False otherwise"""
        return self._exists(self.projects, {'name': name})

    def _exists_section(self, name, project_id):
        """Returns the Todoist section ID if section exists; False otherwise"""
        return self._exists(self.sections, {"name": name, "project_id": project_id})

    def _exists_task(self, project_id, section_id, content):
        """Returns the Todoist task ID if task exists
        in the given project or section; False otherwise"""
        if not project_id and not section_id:
            project_id = self._exists_project('Inbox')

        query = {"project_id": project_id, "section_id": section_id}
        logging.debug(_("get tasks for %s"), query)
        tasks = self.get_tasks(**query)
        logging.debug(_("found %d tasks"), len(tasks))
        return self._exists(tasks, {"content": content})

    def _exists(self, haystack, match):
        item = find_needle_in_haystack(haystack, match)
        if item:
            return getattr(item, "id")
        return False

    def _log_message(self, obj_type, item, obj_id=None, is_new=True):
        msg = ''
        if self.dry_run:
            msg += 'dry run> '
        msg += f"{obj_type}: "
        if is_new:
            msg += '[NEW] '
        msg += f"{item} ({obj_id})"
        return msg

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

    def rollback(self, undo_commands=None):
        """Rollback todoist-template actions"""
        cmds = undo_commands if undo_commands else self.undo_commands
        status = self._do_rollback(cmds)
        if self.dry_run:
            logging.info(_("Rollback status: Dry Run"))
        else:
            logging.info(_("Rollback status: %s"), (_("Success") if status else _("Failure")))
        return status

    def _do_rollback(self, commands):
        logging.debug(_("undo commands: %s"), commands)
        if self.dry_run:
            return False

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
            # when working with the Sync API, changes can be batched into one commit
            # significantly reducing the amount of network calls
            params = {"commands": json.dumps(commands, skipkeys=True, allow_nan=False)}

        response = requests.get(
            f'{self.SYNC_API}/sync',
            headers={"Authorization": f"Bearer {self._token}"},
            params=params,
            timeout=60.0
        )
        return response.json() if response.status_code == 200 else response.content

    def quick_add(self, text):
        """Add a new item using the Quick Add implementation available in the official clients"""
        params = {
            "text": text
        }
        response = requests.get(
            f'{self.SYNC_API}/quick/add',
            headers={"Authorization": f"Bearer {self._token}"},
            params=params,
            timeout=60.0
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise TodoistTemplateError(str(response.content))

    def get_collaborator_id(self, name):
        """Returns collabotor ID by name"""
        coll = [element for element in self.collaborators if element.name.casefold() == name.casefold()]
        return coll[0].id if len(coll) == 1 else None

# ~@:-]
