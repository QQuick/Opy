	.. figure:: http://www.qquick.org/opy.jpg
		:alt: Image of Phaistos Disc
		
		**The famous Phaistos Disc from Crete, obfuscation unbroken after thousands of years.**

Opy will obfuscate your extensive, real world, multi module Python source code for free!
And YOU choose per project what to obfuscate and what not, by editing the config file:

- You can recursively exclude all identifiers of certain modules from obfuscation.
- You can exclude human readable configuration files containing Python code.
- You can use getattr, setattr, exec and eval by excluding the identifiers they use.
- You can even obfuscate module file names and string literals.
- You can run your obfuscated code from any platform.

Bugs fixed:

- erroneous copying of directories above project root fixed
- name of __init__.py files now left unaltered by default
- module directories renamed appropriately
- .pyc files not copied to target directory tree anymore. N.B. Delete them from your existing target trees since they break obfuscation!
- from __future__ import now handled correctly

**Bug reports and feature requests are most welcome and will be taken under serious consideration on a non-committal basis**

What's new:

- pep8_comments option added
- support for obfuscation of names starting with __ added
- license changed from QQuickLicense to Apache 2.0
- empty lines are removed

Installation:

- Download and unzip Opy into an arbitrary directory of your computer.
- You only need the files opy.py and py_config.txt. They are in the opy subdirectory of your unzipped Opy version.
- Put opy.py or a script to launch it in the path of your OS, or simply copy opy.py to the topdirectory of your project.

Use:

- For safety, backup your sourcecode and valuable data to an off-line medium.
- Put a copy of opy_config.txt in the top directory of your project.
- Adapt it to your needs according to the remarks in opy_config.txt.
- This file only contains plain Python and is exec'ed, so you can do anything clever in it.
- Open a command window, go to the top directory of your project and run opy.py from there.
- If the topdirectory of your project is e.g. ../work/project1 then the obfuscation result wil be in ../work/project1_opy.
- Further adapt opy_config.txt until you're satisfied with the result.
- Type 'opy ?' or 'python opy.py ?' (without the quotes) on the command line to display a help text and a reference to the licence.

Important remark:

- Obfuscate your Python code only when stricktly needed. Freedom is one of the main benefits of the Python community. In line with this the source of Opy is not obfuscated.

Example of obfuscated code: ::

	import Tkinter as l1111lll1
	import tkFileDialog
	import os

	from util import *

	from l1l111l import *
	from l1llll1 import *

	l1l1lll1l1l1 = 35
	l1l11l1ll1 = 16

	class l111l1l111l (l1111lll1.Frame, l1lll11ll1):
		def __init__ (self, parent):	
			l1111lll1.Frame.__init__ (self, parent)
			l1lll11ll1.__init__ (self)
			
			self.l1l1ll11llll = []
			
			self.l1l1ll11llll.append (l1111lll1.Frame (self, width = l1l1llll1111, height = l1l11l111l))
			self.l1l1ll11llll [-1] .pack (side = l1llll (u'ࡶࡲࡴࠬ'))
			
			self.l1l1ll1ll11l = l1111lll1.LabelFrame (self, text = l1llll (u'ࡒࡦࡵࡤࡱࡵࡲࡩ࡯ࡩ࠸'), padx = 5)
			self.l1l1ll1ll11l.pack (side = l1llll (u'ࡺ࡯ࡱࠢ'), fill = l1llll (u'ࡦࡴࡺࡨࠧ'), expand = True)
		
Known limitations:

- A comment after a string literal should be preceded by whitespace.
- A ' or " inside a string literal should be escaped with \\ rather then doubled.
- If the pep8_comments option is False (the default), a # in a string literal can only be used at the start, so use 'p''#''r' rather than 'p#r'.
- If the pep8_comments option is set to True, however, only a <blank><blank>#<blank> cannot be used in the middle or at the end of a string literal
- Obfuscation of string literals is unsuitable for sensitive information since it can be trivially broken
- No renaming backdoor support for methods starting with __ (non-overridable methods, also known as private methods)
			
That's it, enjoy!

Jacques de Hooge

jacques.de.hooge@qquick.org

Other packages you might like:

- Lean and mean Python to JavaScript transpiler featuring multiple inheritance https://pypi.python.org/pypi/Transcrypt
- Python PLC simulator with Arduino code generation https://pypi.python.org/pypi/SimPyLC
- Event driven evaluation nodes https://pypi.python.org/pypi/Eden
- A lightweight Python course taking beginners seriously (under construction): https://pypi.python.org/pypi/LightOn

