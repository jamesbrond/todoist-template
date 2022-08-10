"""CSV Template Loader (can load ufficial Todoist templates)"""

import csv
from lib.loader.abstractloader import AbstractTemplateLoader

DEFAULT_PROJECT = "Inbox"

class CsvTemplateLoader(AbstractTemplateLoader):
    """CSV Template Loader (can load ufficial Todoist templates)"""

    def load(self, file):
        reader = csv.DictReader(file, delimiter=',')
        projects = []

        base_prj = {
            DEFAULT_PROJECT: {
                "tasks": []
            }
        }

        curr_prj = None
        curr_sec = None
        for row in reader:
            if row['TYPE'] == "project":
                curr_prj = row['CONTENT']
                projects.append({
                    curr_prj: {
                        "tasks": []
                    }
                })
            elif row['TYPE'] == "section":
                curr_sec = row['CONTENT']
                if not curr_prj:
                    projects.append(base_prj)
                    curr_prj = DEFAULT_PROJECT
                projects[-1][curr_sec] = {
                    "tasks": []
                }
            elif row['TYPE'] == "task":
                task = {
                    "content": row["CONTENT"],
                    "description": row["DESCRIPTION"],
                    "priority": int(row["PRIORITY"]),
                    "due_string": row["DATE"]
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
