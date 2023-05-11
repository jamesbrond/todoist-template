"""CSV Template Loader (can load ufficial Todoist templates)"""

import csv
from lib.loader.abstractloader import AbstractTemplateLoader

DEFAULT_PROJECT = "Inbox"


class CsvTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """CSV Template Loader (can load ufficial Todoist templates)"""

    def load(self, file):
        fieldnames = ['type', 'content', 'priority', 'due_string', 'description']
        reader = csv.DictReader(file, fieldnames, delimiter=',', dialect='excel')
        projects = []

        base_prj = {
            DEFAULT_PROJECT: {
                "tasks": []
            }
        }

        curr_prj = None
        curr_sec = None
        for row in reader:
            if row['type'] == "project":
                curr_prj = row['content']
                projects.append({
                    curr_prj: {
                        "tasks": []
                    }
                })
            elif row['type'] == "section":
                curr_sec = row['content']
                if not curr_prj:
                    projects.append(base_prj)
                    curr_prj = DEFAULT_PROJECT
                projects[-1][curr_sec] = {
                    "tasks": []
                }
            elif row['type'] == "task":
                task = {
                    "content": row["content"],
                    "description": row["description"],
                    "priority": int(row["priority"]),
                    "due_string": row["due_string"]
                }
                if not curr_prj:
                    projects.append(base_prj)
                    curr_prj = DEFAULT_PROJECT
                if curr_sec:
                    projects[-1][curr_sec]["tasks"].append(task)
                else:
                    projects[-1][curr_prj]["tasks"].append(task)

        return projects

# ~@:-]
