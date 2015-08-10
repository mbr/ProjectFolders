import sublime_plugin


class ProjectfolderCommand(sublime_plugin.ApplicationCommand):
    def description(self):
        return 'Open a folder and the associated project'

    def run(self):
        print('Hello, Sublime')
