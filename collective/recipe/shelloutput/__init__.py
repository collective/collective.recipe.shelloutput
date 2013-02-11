# -*- coding: utf-8 -*-
"""Recipe shelloutput"""

import subprocess


class Recipe(object):

    def __init__(self, buildout, name, options):
        cmds = options["commands"].strip()
        output = {}
        if cmds:
            cmds = cmds.split('\n')
            for cmd in cmds:
                if cmd:
                    name, command = cmd.split('=')
                    name = name.strip()
                    command = command.strip()
                    output[name] = self._execute_cmd(name, command)
        options.update(output)

    def _execute_cmd(self, name, command):
        if not command:
            return "Empty command '%s', no output generated." % name
        process = subprocess.Popen([command],
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            return "Error '%s' for command '%s'." % (err.strip(), name)
        return out.strip()

    def install(self):
        return tuple()

    def update(self):
        self.install()
