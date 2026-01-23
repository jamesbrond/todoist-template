"""
CSV Template Loader (can load ufficial Todoist templates)

Example of CSV content:
type,content,priority,due_string,description,labels,assignee
task,Test task 0,1,wed,This is an Inbox task,label1;label2,me

project,Test project,,,,,
section,Test section,,,,,
task,Test task 1,3,today,This is a test,label3;label4,user1
task,Test task 2,4,weekend,This is another test,label5;label6,
"""

import io
import csv
from lib.template.loader.abstractloader import AbstractTemplateLoader, register_loader


DEFAULT_PROJECT = "Inbox"
CSV_DELIMITER = ','
CSV_FORMAT = 'excel'
CSV_FIELDNAMES = ['type', 'content', 'priority', 'due_string', 'description', 'labels', 'assignee']


@register_loader
class CsvTemplateLoader(AbstractTemplateLoader):  # pylint: disable=too-few-public-methods
    """
    CSV Template Loader (can load ufficial Todoist templates)
    All tasks without a project end under the `Inbox` project.
    """

    type = "CSV"
    mimetypes = ["text/csv"]
    extensions = [".csv"]

    def load(self, content: str) -> any:
        reader = csv.DictReader(io.StringIO(content), CSV_FIELDNAMES, delimiter=CSV_DELIMITER, dialect=CSV_FORMAT)
        return self._rows_to_template(reader)

    def _rows_to_template(self, reader: csv.DictReader) -> list:
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
                    "due_string": row["due_string"],
                    "labels": [label.strip() for label in row["labels"].split(';') if label.strip()],
                    "assignee": row["assignee"],
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
