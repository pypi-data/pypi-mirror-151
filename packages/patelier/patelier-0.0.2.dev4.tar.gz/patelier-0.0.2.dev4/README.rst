========
patelier
========

A Japanese text-line analyzing package


Function
-----------------------------

This project is to analyze text lines written in Japanese.

| You can provide the text lines by selecting a text file.
| The text file needs to be encoded in **UTF-8** or **Shift-JIS**.
| Each control code (0x00-0x1f) in the text lines is changed to '▲'.
| For example, a tab code in the text lines is changed to '▲'.

The analysis result is displayed.


**This "patelier" is still under development.**

| *Maybe in the future,*
| *the patelier may be able to display more information*
| *by analyzing text lines.*

I hope the patelier helps you a little.


Development Status
-----------------------------

Pre-Alpha (experiment)


Necessary Environment
-----------------------------

* **Microsoft Windows 10** (Tested with 64 bit version)
* **Python Ver. 3.7 or later** (Tested with Ver. 3.9.0)
* **pip** (Installed with Python) (Tested with Ver. 22.0.4)


Preferred  Environment
-----------------------------

* **Google Chrome** or **Microsoft Edge**


Dependency
-----------------------------

* **eel** (Tested with Ver. 0.14.0)
* **mecab-python3** (MeCab) (Tested with Ver. 1.0.5)
* **natsort** (Tested with Ver. 8.1.0)
* **pyperclip** (Tested with Ver. 1.8.2)
* **python-docx** (Tested with Ver. 0.8.11)
* **pywin32** (win32com) (Tested with Ver. 304)
* **regex** (Tested with Ver. 2022.4.24)


Setup
-----------------------------

command::

    py -m pip install patelier

    (for upgrade)
    py -m pip install -U patelier


Usage
-----------------------------

command::

    patelier


Auther
-----------------------------

K2UNIT


License
-----------------------------

This software is released under the MIT License, see LICENSE.txt.


Notes
-----------------------------

This "patelier" is supposed to be used in Japan.

| The patelier is still under development.
| So, the patelier may suddenly be unpublished,
| and the license terms may be changed
| in the future (eg to the Apache license 2.0, etc.).
