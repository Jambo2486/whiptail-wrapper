# Simple Whiptail wrapper
## Requires Whiptail to be installed!
### To do this on Replit:
- Open the shell tab on Replit
- Enter `whiptail`
- Hit enter
- Paste this `wiptail.py` into your Replit files
- See example code:
## Examples:
```from whiptail import Box```
### Inline:
```print(Box("text", optional_flags = "argument").prompt("options"))```
### Block:
```
box = Box("text", optional_flags = "argument")  
print(box.prompt("options"))
```
