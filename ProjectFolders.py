import json
import os
import subprocess

import sublime
import sublime_plugin


def open_project_in_window(window, project_file, subl='subl'):
    window.run_command("close_project")
    window.run_command("close_all")

    subprocess.check_call([subl, '--project', project_file, ])


def get_settings():
    return sublime.load_settings('ProjectFolders.sublime-settings')


def get_project_dirs():
    return [os.path.expanduser(d)
            for d in get_settings().get('project_dirs', [])
            if os.path.exists(os.path.expanduser(d))]


class ProjectfolderCommand(sublime_plugin.WindowCommand):
    def description(self):
        return 'Open a folder and the associated project'

    def open_project_folder(self, path):
        # information available for pathname generation
        d = {
            'basename': os.path.basename(path),
            'path': path,
            'dirname': os.path.dirname(path),
        }

        project_file = get_settings().get('project_file_format').format(d)

        # if the project does not exist, create it
        if not os.path.exists(project_file):
            with open(project_file, 'w') as out:
                proj = {'folders': [{'path': path}]}
                json.dump(proj, out)

        open_project_in_window(self.window, project_file)

    def create_project_folder(self, path):
        def on_done(s):
            if not s:
                sublime.status_message('No input, no new project created')
                return

            dn = os.path.join(os.path.expanduser(path), s)
            os.mkdir(dn)
            sublime.status_message('Created {}'.format(dn))

            # now that the folder has been created, open it
            self.open_project_folder(dn)

        self.window.show_input_panel(path,
                                     '',
                                     on_done,
                                     on_change=lambda s: None,
                                     on_cancel=lambda: None)

    def run(self):
        # collect list of packages
        dirs = get_project_dirs()

        entries = ['[+] Create new folder in {}'.format(d) for d in dirs]

        for basedir in dirs:
            sub_entries = []
            for dn in os.listdir(os.path.expanduser(basedir)):
                sub_entries.append(os.path.join(basedir, dn))
            entries.extend(sorted(sub_entries))

        def _open_entry(n):
            if n == -1:
                return

            if n < len(dirs):
                self.create_project_folder(dirs[n])
            else:
                self.open_project_folder(os.path.expanduser(entries[n]))

        self.window.show_quick_panel(entries, _open_entry)
