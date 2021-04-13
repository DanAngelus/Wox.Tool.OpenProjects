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

    def generateResponse(self, root, root_dir_arr):
        filepath = re.split('\\\\|/', root)
        return {
            'Title': f"{''.join(str(e) + ' / ' for e in [p for p in filepath if p not in root_dir_arr])}"[:-2],
            'SubTitle': f'Open: {root} in IntelliJ IDEA',
            'IcoPath': 'Images/pic.png',
            'JsonRPCAction': {
                'method': 'action',
                'parameters': [root],
                'dontHideAfterAction': False
            }
        }

    def query(self, user_input):
        responses = []
        root_dir_arr = re.split('\\\\|/', self.root_dir)
        for root, dirs, files in os.walk(self.root_dir, topdown=True):
            dirs[:] = [d for d in dirs if d not in self.exclude]
            if '.idea' in next(os.walk(root))[1] and (not user_input or root.lower().find(user_input.lower()) > -1):
                responses.append(self.generateResponse(root, root_dir_arr))

                # Limited to 10 to improve performance
                if len(responses) >= 15:
                    return responses

        return responses

    def action(self, project):
        Popen(["idea64.exe", f"{project}"])

if __name__ == '__main__':
    OpenProject()

