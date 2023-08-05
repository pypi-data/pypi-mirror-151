# TerminalPyth

### Library that allows you to call terminal commands in python whithout discarding director changes (unlike os.system() method does).

## `Installation:`

    $ pip install terminalpyth

## `Usage:`

    import terminalpy

Create a terminalpy object. Pass True or False as argument if you want (or not) to have back the output.

    trm = terminalpy.Terminal(output=True)

Only one straight-forward method: type. Pass inside it the command you want to be executed.

    output = trm.type('pwd')

    # in this case, returns path to the current directory,
    # which in this case is stored in "output"

It works with pretty much every terminal command. 

To use "sudo", if you are not in a terminal session itself, you must add the "-S" option, 
to read the password from IDE (e.g. Pycharm).

    trm.clear()

This command clears the memory of the directory changes, returning back to the project foler.

    trm.setOutput(output=False)

Changes the state of the return action. If "False", there will be no return value, otherwise there will. \
The method allows to change the state during the session.

## `Example:`

Imagine a basic directory tree:

    - home
        - python
            - project1
                - main.py
            - prokect2
                - main2.py
        - cpp
            - project3
                
This is the difference between TerminalPyth and os, receiving the same exact instructions:

    # /home/python/project1/main.py
    import terminalpy as tp
    
    term = tp.Terminal(output=True)
    
    path = term.type('pwd')
    print(path)
    # output: /home/python/project1

    term.type('cd ..')
    print(term.type('ls')
    # output:   project1
    #           project2

    term.type('cd ..')
    term.type('cd cpp')
    print(term.type('pwd'))
    # output: /home/cpp

    term.clear()
    print(term.type('pwd'))
    # output: /home/python/project1

    --------------------------------

    # /home/python/project2/main2.py
    import os

    os.system('pwd')
    # output: /home/python/project2

    os.system('cd ..')
    os.system('ls')
    # output: main2.py

    os.system('cd ..')
    os.system('cd c++') # Error: The directory 'cpp' does not exist
    os.system('pwd')
    # output: /home/python/project2


The main differences between TerminalPyth and os.system(): \
    - TerminalPyth allows multiple direcotry changes \
    - TerminalPyth allows to store the output in a variable \
    - TerminalPyth lets you chose if return the output or not \
    - os.system() prints its output always, in any case \
    - os.system() doesn't allow to store the output \
    - os.system() doesn't allow multiple directory change
