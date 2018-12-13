'''_opy_Copyright 2014, 2015, 2016, 2017, 2018 Jacques de Hooge, GEATEC engineering, www.geatec.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

'''This module makes it possible to use Opy as part of a Python application.

The API was kept utterly simple and non-intrusive.
It just mimics command line activation without starting a new interpreter.
So the normal docs about the Opy command line apply.

Just import this module and then call the 'run' function with as parameters
the strings that normally would have been the command line
arguments to mypy.

Function 'run' returns a tuple
    (<normal_report>, <error_report>, <exit_status>),
in which
    - <normal_report> is what Opy normally writes to sys.stdout
    - <error_report> is what Opy normally writes to sys.stderr
    - exit_status is twhat Opy normally returns to the operating system

Trivial example of code using this module:

import sys
from opy import api

result = api.run(sys.argv[1:])

if result[0]:
    print('\nObfuscation report:\n')
    print(result[0])  # stdout

if result[1]:
    print('\nError report:\n')
    print(result[1])  # stderr

print ('\nExit status:', result[2])
'''

import sys
import io
import traceback

from .opy import main

def run (*params):
    sys.argv = [''] + list (params)
    
    old_stdout = sys.stdout
    new_stdout = io.StringIO ()
    #sys.stdout = new_stdout

    old_stderr = sys.stderr
    new_stderr = io.StringIO ()
    sys.stderr = new_stderr
    
    try:
        exit_status = 0
        main ()
    except SystemExit as system_exit:
        exit_status = system_exit.code
    except Exception as exception:
        print (traceback.format_exc ())
        
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    return new_stdout.getvalue (), new_stderr.getvalue (), exit_status

    