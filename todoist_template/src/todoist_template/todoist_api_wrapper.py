"""Layer module to handle Todoist API"""
from todoist_template.pokemon_exception import pokemon_exception_handler_class_decorator
import logging
import json
import ssl
import httpx
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from todoist_api_python._core.endpoints import API_URL
from todoist_template.utils import find_needle_in_haystack, uid
from todoist_template.i18n import _t


@pokemon_exception_handler_class_decorator
class TodoistAPIWrapper(TodoistAPI):
    """Layer class to handle Todoist API"""

    def __init__(self, cfg):
        self._ssl_ca_root_file = getattr(getattr(cfg, "security", None), "ssl_ca_root_file", None)

        client = None
        if self._ssl_ca_root_file:
            try:
                logging.debug('Adding custom certificates `%s`', self._ssl_ca_root_file)
                client = httpx.Client(verify=self._ssl_ca_root_file)
            except (OSError, ssl.SSLError) as exc:
                logging.warning(_t("Failed to load custom certificate from file: `%s`"), self._ssl_ca_root_file)
                logging.warning(exc)
                self._ssl_ca_root_file = None

        super().__init__(cfg.config.api_token, None, client=client)

        is_undo = cfg.is_undo
        self._is_dry_run = cfg.dry_run
        self._undo_commands = []

        if not is_undo:
            self._projects = self._get_projects()
            self._sections = self._get_sections()

    def project(self, project):
        """
        Create a new project unless a project with the same name already exists.
        In any case it returns the project ID
        """
        project_id = self._exists_project(project['name'])
        if project_id:
            logging.info(self._log_message(_t('Project'), project['name'], project_id, False))
            self._collaborators = self._get_collaborators(project_id)
            return project_id

        self._collaborators = []
        logging.info(self._log_message(_t('Project'), project['name']))
        if self._is_dry_run:
            return None
        new_project = self.add_project(**project)
        self._projects.append(new_project)
        self._undo_commands.append(self._add_undo_command("project_delete", new_project.id))
        return new_project.id

    def section(self, section):
        """
        Create a new section unless a section with the same name in the same project
        already exists. In any case it returns the section ID
        """
        section_id = self._exists_section(section['name'], section['project_id'])
        if section_id:
            logging.info(self._log_message(_t('Section'), section['name'], section_id, False))
            return section_id

        logging.info(self._log_message(_t('Section'), section['name']))
        if self._is_dry_run:
            return None
        new_section = self.add_section(**section)
        self._sections.append(new_section)
        self._undo_commands.append(self._add_undo_command("section_delete", new_section.id))
        return new_section.id

    def task(self, task, update=False):
        """Create or update task"""
        if task.get('assignee'):
            task['assignee_id'] = self.get_collaborator_id(task.get('assignee'))
            if not task['assignee_id']:
                logging.warning(_t("Assignee %s not found in project %s"), task.get('assignee'), task.get('project_id'))
            del task['assignee']  # remove assignee name to avoid API error

        if update:
            task_id = self._exists_task(
                task.get('project_id'),
                task.get('section_id'),
                task.get('content'))
        else:
            task_id = None

        if self._is_dry_run:
            logging.info(self._log_message(_t('Task'), task['content'], task_id, task_id is None))
            return None

        if task_id:
            is_new = False
            original_task = self.get_task(task_id=task_id).to_dict()
            if self.update_task(task_id=task_id, **task):
                logging.debug("update task: %s", str(task_id))
                self._undo_commands.append(self._add_undo_command("item_update", task_id, original_task))
        else:
            is_new = True
            new_task = self.add_task(**task)
            logging.debug("created new task: %s", task)
            self._undo_commands.append(self._add_undo_command("item_delete", new_task.id))
            task_id = new_task.id

        logging.info(self._log_message(_t('Task'), task['content'], task_id, is_new))
        return task_id

    def _get_projects(self):
        logging.debug("Retrieve existing projects and sections from Todoist")
        return [p for page in self.get_projects() for p in page]

    def _get_sections(self):
        logging.debug("Retrieve existing sections from Todoist")
        return [s for page in self.get_sections() for s in page]

    def _get_tasks(self, query: dict[str, str]):
        logging.debug("Retrieve existing tasks from Todoist for query %s", query)
        return [t for page in self.get_tasks(**query) for t in page]

    def _get_collaborators(self, project_id):
        logging.debug("Retrieve existing collaborators from Todoist for project %s", project_id)
        return [c for page in self.get_collaborators(project_id) for c in page]

    def _exists_project(self, name):
        """Returns the Todoist project ID if project exists; False otherwise"""
        return self._exists(self._projects, {'name': name})

    def _exists_section(self, name, project_id):
        """Returns the Todoist section ID if section exists; False otherwise"""
        return self._exists(self._sections, {"name": name, "project_id": project_id})

    def _exists_task(self, project_id: str, section_id: str, content):
        """Returns the Todoist task ID if task exists
        in the given project or section; False otherwise"""
        prjid = self._exists_project('Inbox') if not project_id and not section_id else project_id
        if not prjid:
            raise ValueError(_t("Project ID is required to check for existing tasks"))

        query = {"project_id": prjid, "section_id": section_id}
        tasks = self._get_tasks(query)
        logging.debug("found %d tasks", len(tasks))
        return self._exists(tasks, {"content": content})

    def _exists(self, haystack, match):
        item = find_needle_in_haystack(haystack, match)
        if item:
            return item.id
        return False

    def _log_message(self, obj_type, item, obj_id=None, is_new=True):
        msg = ''
        if self._is_dry_run:
            msg += _t('dry run>') + ' '
        msg += f"{obj_type}: "
        if is_new:
            msg += _t('[NEW]') + ' '
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

    def rollback(self, undo_commands=None, is_dry_run=False) -> bool:
        """Rollback todoist-template actions"""
        cmds = undo_commands if undo_commands else self._undo_commands
        status = self._do_rollback(cmds)
        if is_dry_run:
            logging.info(_t("dry run>") + ' ' + _t("Rollback status: Nothing done"))
        else:
            logging.info(_t("Rollback status: %s"), (_t("Success") if status else _t("Failure")))
        return status

    def _do_rollback(self, commands):
        logging.debug("undo commands: %s", commands)
        if self._is_dry_run:
            return False

        response = self._sync(commands)
        logging.debug("undo response %s", response)

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

        response = self._client.post(
            f'{API_URL}/sync',
            headers={"Authorization": f"Bearer {self._token}"},
            data=params,
            timeout=60.0,
        )
        if response.status_code != 200:
            logging.warning(self._log_message(_t("request returning status code: "), response.status_code))
            logging.warning(str(response.content))
        return response.json() if response.status_code == 200 else response.content

    def quick_add(self, text) -> str | None:
        """Add a new item using the Quick Add implementation available in the official clients"""
        # The text of the task that is parsed. It can include a due date in free form text,
        # a project name starting with the # character (without spaces),
        # a label starting with the @ character,
        # an assignee starting with the + character,
        # a priority (e.g., p1),
        # a deadline between {} (e.g. {in 3 days}),
        # or a description starting from // until the end of the text.

        if self._is_dry_run:
            logging.info(self._log_message(_t('Task'), text, None, True))
            return None

        quick: Task = self.add_task_quick(text)
        logging.info(self._log_message(_t('Task'), quick.content, quick.id, True))
        return quick.id

    def get_collaborator_id(self, name):
        """Returns collaborator ID by name"""
        coll = [element for element in self._collaborators if element.name.casefold() == name.casefold()]
        # what if we have more collaborators with the same name?
        return coll[0].id if len(coll) == 1 else None

# ~@:-]
