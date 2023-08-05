import yaml
from spacectl.lib.apply.task import Task
from spacectl.lib.apply import store
from spacectl.lib.parser import apply_manifest
from spacectl.modules import MODULES
from spacectl.lib.output import echo
import click
from pathlib import Path
import os.path
from spaceone.core import utils
from spacectl.lib.parser.default import parse_uses
import os


class TaskManager:

    def __init__(self, silent):
        self.task_queue = list()  # Task Queue
        self.silent = silent

    def load(self, file_path):
        data = utils.load_yaml_from_file(file_path)
        # data = yaml.safe_load(file_path)

        for import_file in data.get('import', []):
            # import file path is relative to current file_path
            absolute_location = Path(file_path).parent
            self.load(os.path.join(absolute_location, import_file))

        store.set_var(data.get('var', {}))
        store.set_env(data.get('env', {}))

        for task in data.get("tasks", []):
            self.task_queue.append(task)

    def run(self):
        for task in self.task_queue:
            context = {
                "var": store.get_var(),
                "env": store.get_env(),
                "tasks": store.get_task_results(),
                # "self": task,
            }
            apply_manifest.apply_template(task, task.get("id", "anonymous_task_id"))
            module = parse_uses(task["uses"])
            task_module = MODULES.get(module)

            if task_module:
                t = task_module(task, silent=self.silent)
                t.execute()
            else:
                raise Exception(f'Not found Module: {module}')
