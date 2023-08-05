![bashtable](https://user-images.githubusercontent.com/42397332/162611617-8835e233-3c59-4f8e-9846-c6c4e2add4ae.png)

<div align="center">
	<br>
	<img src="https://img.shields.io/github/workflow/status/rackodo/bashtable/Upload%20Python%20Package?label=Package%20Status&style=for-the-badge&logo=python&logoColor=white">
	<img src="https://img.shields.io/github/v/tag/rackodo/bashtable?style=for-the-badge">
	<img src="https://img.shields.io/github/release-date/rackodo/bashtable?style=for-the-badge">
	<img src="https://img.shields.io/github/commit-activity/w/rackodo/bashtable?style=for-the-badge">
	<br><br>
</div>

Bashtable is a tables package for Python that provides a simple and easy to use system for creating simplistic and professional looking tables to use in your Python programs.

Bashtable is inspired by [Kyostenas' prettyTables](https://github.com/Kyostenas/prettyTables) and is intended as a simpler way to display data in the Python console.

# Table of Contents
- [Installation](#installation)
  * [Using pip](#using-pip)
  * [Using setup.py](#using-setuppy)
- [Usage](#usage)
  * [Basic bashtable](#basic-bashtable)
  * [Adding column titles](#adding-column-titles)
- [Support and Contributions](#support-and-contributions)

# Installation
## Using pip
Run `python -m pip install bashtable` in the context of your choice, and Bashtable will be installed into your Python installation's site-packages.
## Using setup.py
Download the latest release's source code and run `python setup.py install` in the root directory.

# Usage
## Basic bashtable

**Input**
```python
from bashtable import bashtable

table = bashtable()
table.setData(0, "Bash", "Elliott", "17")
table.setData(1, "Jane", "Doe", "21")
table.setData(2, "John", "Doe", "21")
table.draw()
```

**Output**
```
╔══════╦═════════╦════╗
║      ║         ║    ║
╠══════╬═════════╬════╣
│ Bash │ Elliott │ 17 │
├──────┼─────────┼────┤
│ Jane │ Doe     │ 21 │
├──────┼─────────┼────┤
│ John │ Doe     │ 21 │
╚──────┴─────────┴────╝
```

## Adding column titles

**Input**
```python
from bashtable import bashtable

table = bashtable()
table.setColumnTitle(0, "First Name")
table.setColumnTitle(1, "Last Name")
table.setColumnTitle(2, "Age")

table.setData(0, "Bash", "Elliott", "17")
table.setData(1, "Jane", "Doe", "21")
table.setData(2, "John", "Doe", "21")
table.draw()
```

**Output**
```
╔════════════╦═══════════╦═════╗
║ First Name ║ Last Name ║ Age ║
╠════════════╬═══════════╬═════╣
│ Bash       │ Elliott   │ 17  │
├────────────┼───────────┼─────┤
│ Jane       │ Doe       │ 21  │
├────────────┼───────────┼─────┤
│ John       │ Doe       │ 21  │
╚────────────┴───────────┴─────╝
```

# Support and Contributions
If you have any suggestions for Bashtable or want to fork Bashtable to improve upon it or add any features, feel free to do so and even make a pull request! I appreciate each and every contribution made.

If you've found a bug, please make an issue so I can work towards fixing it. I am also reachable by email at spicethings9@gmail.com.

# Credits
Credit to [@Kyostenas](https://github.com/Kyostenas) and his package [prettyTables](https://github.com/Kyostenas/prettyTables) for the inspiration to create Bashtable.
