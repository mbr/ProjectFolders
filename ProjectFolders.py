import json
import os
import subprocess

import sublime_plugin


def open_project_in_window(window, project_file, subl='subl'):
    window.run_command("close_project")
    window.run_command("close_all")

    subprocess.check_call([subl, '--project', project_file, ])


class ProjectfolderCommand(sublime_plugin.WindowCommand):
    def description(self):
        return 'Open a folder and the associated project'

    def open_project_folder(self, path):
        print('opening project associated with {}'.format(path))
        basename = os.path.basename(path)
        project_file = os.path.join(path, basename + '.sublime-project')
        print('project file: {}'.format(project_file))

        # if the project does not exist, create it
        if not os.path.exists(project_file):
            with open(project_file, 'w') as out:
                json.dump({}, out)

        open_project_in_window(self.window, project_file)

    def run(self):
        # collect list of packages
        dirs = ['~']

        entries = []

        for basedir in dirs:
            for dn in os.listdir(os.path.expanduser(basedir)):
                entries.append(os.path.join(basedir, dn))

        entries.sort()

        def _open_entry(n):
            if n == -1:
                return

            self.open_project_folder(os.path.expanduser(entries[n]))

        self.window.show_quick_panel(entries, _open_entry)
