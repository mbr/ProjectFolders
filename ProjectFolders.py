import os

import sublime
import sublime_plugin


class ProjectfolderCommand(sublime_plugin.WindowCommand):
    def description(self):
        return 'Open a folder and the associated project'

    def open_project_folder(self, path):
        print('opening project associated with {}'.format(path))

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

            self.open_project_folder(entries[n])

        self.window.show_quick_panel(entries, _open_entry)
