from wox import Wox
from subprocess import Popen
import os
import re
import json


class OpenProject(Wox):

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)
        root_dir = settings['projectsDir']

    exclude = ['.idea', '.git', 'build', 'node_modules', 'target', 'gradle', '.gradle', '.mvn', 'src', 'out', 'dist', 'etc']

    def query(self, user_input):
        responses = []
        root_dir_arr = re.split('\\\\|/', self.root_dir)
        for root, dirs, files in os.walk(self.root_dir, topdown=True):
            dirs[:] = [d for d in dirs if d not in self.exclude]
            filtered_files = [f for f in files if f.endswith('.iml')]
            if dirs and filtered_files:
                filepath = re.split('\\\\|/', root)
                # ToDo :: Update this to check every section of filepath
                if not user_input or filepath[-1].startswith(user_input):
                    responses.append({
                        'Title': f"{''.join(str(e) + ' / ' for e in [p for p in filepath if p not in root_dir_arr])}",
                        'SubTitle': f'Open: {root} in IntelliJ IDEA',
                        'IcoPath': 'Images/pic.png',
                        'JsonRPCAction': {
                            'method': 'action',
                            'parameters': [root],
                            'dontHideAfterAction': False
                        }
                    })

        return responses

    def action(self, project):
        # FixMe :: This doesn't work asynchronously
        Popen(["idea.cmd", project])

if __name__ == '__main__':
    OpenProject()
