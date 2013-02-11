Exec shell commands and reuse the output
========================================

This recipe is for execute shell commands and get the output in another part of
the buildout. The commands are defined in a section called commands, one per
line and the output can be referenced from other parts using the ${...} syntax.

    >>> write('dummy.py',
    ... '''
    ... class Recipe(object):
    ...
    ...     def __init__(self, buildout, name, options):
    ...         self.options = options
    ...
    ...     def install(self):
    ...         if 'output_1' in self.options:
    ...             print self.options['output_1']
    ...         if 'output_2' in self.options:
    ...             print self.options['output_2']
    ...         return ()
    ...
    ...     def update(self):
    ...         pass
    ... ''')

    >>> write('setup.py',
    ... '''
    ... from setuptools import setup
    ...
    ... setup(name='dummyrecipe',
    ...       entry_points = {'zc.buildout': ['default = dummy:Recipe']})
    ... ''')

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... develop = .
    ... parts =
    ...     shelloutput
    ...     use-shelloutput
    ... offline = true
    ...
    ... [shelloutput]
    ... recipe = collective.recipe.shelloutput
    ... commands =
    ...     echo_1 = echo 'ECHO'
    ...     echo_2 = echo 'The shell says: hello.'
    ...
    ... [use-shelloutput]
    ... recipe = dummyrecipe
    ... output_1 = ${shelloutput:echo_1}
    ... output_2 = ${shelloutput:echo_2}
    ... ''')

    >>> print system(join('bin', 'buildout')),
    Develop: '/sample-buildout/.'
    Installing shelloutput.
    Installing use-shelloutput.
    ECHO
    The shell says: hello.


If we give an empty command we get a hint.

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... develop = .
    ... parts =
    ...     shelloutput
    ...     use-shelloutput
    ... offline = true
    ...
    ... [shelloutput]
    ... recipe = collective.recipe.shelloutput
    ... commands =
    ...     empty-cmd =
    ...
    ... [use-shelloutput]
    ... recipe = dummyrecipe
    ... output_1 = ${shelloutput:empty-cmd}
    ... ''')

  >>> print system(join('bin', 'buildout')),
    Develop: '/sample-buildout/.'
    Uninstalling use-shelloutput.
    Uninstalling shelloutput.
    Installing shelloutput.
    Installing use-shelloutput.
    Empty command 'empty-cmd', no output generated.


If the execution of a command generates an error, we get the error message.

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... develop = .
    ... parts =
    ...     shelloutput
    ...     use-shelloutput
    ... offline = true
    ...
    ... [shelloutput]
    ... recipe = collective.recipe.shelloutput
    ... commands =
    ...     date = date -invalid-option
    ...
    ... [use-shelloutput]
    ... recipe = dummyrecipe
    ... output_1 = ${shelloutput:date}
    ... ''')

    >>> print system(join('bin', 'buildout')),
    Develop: '/sample-buildout/.'
    Uninstalling use-shelloutput.
    Uninstalling shelloutput.
    Installing shelloutput.
    Installing use-shelloutput.
    Error 'date: invalid option ... for command 'date'...
