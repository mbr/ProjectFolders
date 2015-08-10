import json
import os
import subprocess

import sublime
import sublime_plugin


def open_project_in_window(window, project_file, subl='subl'):
    window.run_command("close_project")
    window.run_command("close_all")

    subprocess.check_call([subl, '--project', project_file, ])

# settings are reloaded automatically, no need to fetch these every time
settings = sublime.load_settings('ProjectFolders.sublime-settings')


class ProjectfolderCommand(sublime_plugin.WindowCommand):
    def description(self):
        return 'Open a folder and the associated project'

    def open_project_folder(self, path):
        print('opening project associated with {}'.format(path))
        # information available for pathname generation
        d = {
            'basename': os.path.basename(path),
            'path': path,
            'dirname': os.path.dirname(path),
        }

        project_file = settings.get('project_file_format').format(d)
        print('project file: {}'.format(project_file))

        # if the project does not exist, create it
        if not os.path.exists(project_file):
            with open(project_file, 'w') as out:
                proj = {'folders': [{'path': path}]}
                json.dump(proj, out)

        open_project_in_window(self.window, project_file)

    def run(self):
        # collect list of packages
        dirs = settings.get('project_dirs')

        entries = []

        for basedir in dirs:
            sub_entries = []
            for dn in os.listdir(os.path.expanduser(basedir)):
                sub_entries.append(os.path.join(basedir, dn))
            entries.extend(sorted(sub_entries))

        def _open_entry(n):
            if n == -1:
                return

            self.open_project_folder(os.path.expanduser(entries[n]))

        self.window.show_quick_panel(entries, _open_entry)
