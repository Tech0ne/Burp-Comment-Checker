# Burp-Comment-Checker
Simple Burp plugin that aim to extract comments out of web pages

---

## How to install ?

To use this plugin, you need to setup the burp plugin environment (see [here](https://portswigger.net/burp/extender/writing-your-first-burp-suite-extension#tab-content-codetype2))

Next, get the `comment-checker.py` file and put it on the burp extentions directory.

Enable the extention in the "Extentions" burp tab.

If no error is raised, you are ready to go !

---

## How to use ?

To use this extention, you simply need to go in any request in the "Target" tab, right click, and select "Extensions > Comment scanner > Scan for comments".

It will prompt the results in the Extensions tab, under Output.

_Please note that this configuration is temporary, and might probably change soon, for a more usable way to scan_

---

## TODO

- [ ] Change use (Make it more user-friendly)
- [ ] Change output (Another window ?)
- [ ] Add full check (When you ask to scan one page, scan all found pages of that target)
