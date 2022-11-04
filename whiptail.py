"""Simple Whiptail wrapper

# Requires Whiptail to be installed!
# To do this on Replit:
- Open the shell tab on Replit
- Enter `whiptail`
- Hit enter
- Paste this `wiptail.py` into your Replit files
- See example code:

# Examples:
```from whiptail import Box```

## Inline:
```print(Box("text", optional_flags = "argument").prompt("options"))```

## Block:
```
box = Box("text", optional_flags = "argument")  
print(box.prompt("options"))
```
"""

import os
from subprocess import Popen, PIPE

debug = False

def default_box_size():
	terminal_size = os.get_terminal_size()
	width = int(terminal_size[0]*0.6)
	height = int(terminal_size[1]*0.6)
	return width, height
	
def splice_lists(*lists):
	for l in range(len(lists)):
		if lists[l] is None: lists.remove(l)
	sub_num = len(lists)
	sub_len = len(lists[0])
	assert all(map(lambda sub:len(sub)==sub_len, lists[1:])), "All lists must be the same length"
	list_ = [None] * (sub_len * sub_num)
	for i in range(sub_num):
		list_[i::sub_num] = lists[i]
	return list_

class Flag:
	def __init__(self, name, *options):
		self.name = name
		self.options = options
	
	def resolve(self):
		# for option in self.options:
		return ["--" + self.name] + list(self.options)

class Box:
	def __init__(self,
				 text = "",
				 width = default_box_size()[0],
				 height = default_box_size()[1],
				 title = None,
				 backtitle = None,
				 full_buttons = False
				):
		self.text = "" if len(text) == 0 else "\n" + text
		self.width = width
		self.height = height
		flags = []
		if title is not None: flags.append(Flag("title", title))
		if backtitle is not None: flags.append(Flag("backtitle", backtitle))
		if full_buttons: flags.append(Flag("fb"))
		self.flags = flags

	def run(self, flags):
		# based on https://github.com/marwano/whiptail/blob/master/whiptail.py#L31
		resolved = []
		for flag in flags:
			resolved = resolved + flag.resolve()
		command = ["whiptail"] + [str(i) for i in resolved]
		if debug: input(command)
		p = Popen(command, stderr=PIPE)
		out, entry = p.communicate()
		return p.returncode, entry
	
	def message(self, ok = "Ok"):
		self.flags.append(Flag("msgbox", self.text, self.height, self.width))
		self.flags.append(Flag("ok-button", ok))
		self.run(self.flags)

	def yesno(self, yes = "Yes", no = "No", defaultno = False) -> bool:
		self.flags.append(Flag("yesno", self.text, self.height, self.width))
		self.flags.append(Flag("yes-button", yes))
		self.flags.append(Flag("no-button", no))
		return False if self.run(self.flags)[0] else True

	def input(self, init = None, password = False, ok = "Ok", cancel = "Cancel") -> str:
		if init is not None:
			self.flags.append(Flag("passwordbox" if password else "inputbox", self.text, self.height, self.width, init))
		else:
			self.flags.append(Flag("passwordbox" if password else "inputbox", self.text, self.height, self.width))
		self.flags.append(Flag("ok-button", ok))
		self.flags.append(Flag("cancel-button", cancel)) if cancel is not None else self.flags.append(Flag("nocancel"))
		returncode, entry = self.run(self.flags)
		if returncode: return False
		else: return entry.decode()

	def menu(self, list_height, tags, items = None, ok = "Ok", cancel = None) -> str:
		list_ = splice_lists(tags, tags if items is None else items)
		if items is None: self.flags.append(Flag("noitem"))
		self.flags.append(Flag("menu", self.text, self.height, self.width, list_height, *list_))
		self.flags.append(Flag("ok-button", ok))
		self.flags.append(Flag("cancel-button", cancel)) if cancel is not None else self.flags.append(Flag("nocancel"))
		returncode, entry = self.run(self.flags)
		if returncode: return False
		else: return entry.decode()

	# Cancel is impossible to navigate to, as far as I can tell
	def multi_choice(self, list_height, status, tags, items = None, ok = "Ok", cancel = None) -> str:
		list_ = splice_lists(tags, tags if items is None else items, status)
		if items is None: self.flags.append(Flag("noitem"))
		self.flags.append(Flag("checklist", self.text, self.height, self.width, list_height, *list_))
		self.flags.append(Flag("ok-button", ok))
		self.flags.append(Flag("cancel-button", cancel)) if cancel is not None else self.flags.append(Flag("nocancel"))
		returncode, entry = self.run(self.flags)
		if returncode: return False
		else: return entry.decode()

	# Cancel is impossible to navigate to, as far as I can tell
	def single_choice(self, list_height, status, tags, items = None, ok = "Ok", cancel = None) -> str:
		list_ = splice_lists(tags, tags if items is None else items, status)
		if items is None: self.flags.append(Flag("noitem"))
		self.flags.append(Flag("radiolist", self.text, self.height, self.width, list_height, *list_))
		self.flags.append(Flag("ok-button", ok))
		self.flags.append(Flag("cancel-button", cancel)) if cancel is not None else self.flags.append(Flag("nocancel"))
		returncode, entry = self.run(self.flags)
		if returncode: return False
		else: return entry.decode()
