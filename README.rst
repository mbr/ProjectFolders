Project Folders for Sublime Text
================================

Creating projects in Sublime can be tedious, especially if you are using your
filesystem as your project manager already. This plugin maps your filesystem
structure to sublime projects, automatically creating ``.sublime-project``
files as needed.


How it works
------------
Once you launch the ``projectfolder`` command, a quick panel appears listing
all subdirectories of all of your directories that contain projects (per
default, this is your homefolder. See ``project_dirs`` in the configuration
file).

After a directory has been selected, ProjectFolders will try to find a
project file for it; if none is found, an empty one is created. These
``.sublime-project`` files live inside these directories by default, this
behaviour can be configured as well (see ``project_file_format`` in the
configuration file).


Key bindings
------------

If you are using ProjectFolders as a replacement for Sublime's own quick
projects access, which is bound to ``ctrl+alt+p`` by default, add the following
to your ``Default (...).sublime-keymap`` in your ``User`` package:

.. code-block:: json

    [
      {
        "keys": ["ctrl+alt+p"],
        "command": "projectfolder"
      }
    ]


Configuration
-------------

Settings are read from ``ProjectFolders.sublime-settings`` in your ``User``
package:

------------------- -----------
Setting             Description
------------------- -----------
project_dirs        A list of directories to look in for projects. ``~`` will
                    be expanded to ``$HOME``.
project_file_format The format string to create the filename of the project
                    file. Supports ``{0[path]}``, ``{0[basename]}`` and ``{0
                    [dirname]}``. Can be used to put all project files into a
                    single directory by not using ``{0[path]}``.


Open issues
-----------

Currently, ProjectFolders is not on PackageControl and has no Windows support.
