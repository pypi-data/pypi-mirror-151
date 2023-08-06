# Terminarty

###### A simple CLI helper for Python

[![License: MIT](https://img.shields.io/pypi/l/terminarty)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/terminarty)](https://pypi.org/project/terminarty/)
[![Python versions](https://img.shields.io/pypi/pyversions/terminarty)](https://python.org/)
[![Downloads](https://img.shields.io/pypi/dm/terminarty)](https://pypi.org/project/terminarty/)

## Installation

```bash
pip install terminarty
```

## Features

**Inputs**

```python
from terminarty import Terminal

terminal = Terminal()

name = terminal.input("What is your name?")
```

!["What is yout name?"](https://imgur.com/huf4E5P.png)

**Choises**

```python
from terminarty import Terminal

terminal = Terminal()
choise = terminal.choise("What is your favorite color?", ["red", "green", "blue"])

if choise == "green":
    print("I like green too!")
else:
    print("Ok.")
```

!["What is your favorite color?" (red, green, blue)](https://imgur.com/NQwkfj6.png)

**Selects**

```python
from terminarty import Terminal

terminal = Terminal()
choise = terminal.select("What is your favorite color?", ["red", "green", "blue"])

if choise == "green":
    print("I like green too!")
else:
    print("Ok.")
```

_Up and down arrows to navigate. Enter to select._

!["What is your favorite color?" (red, green, blue)](https://media.giphy.com/media/UzI2TazF6lCC0Jz9dJ/giphy.gif)

**Text Boxes**

```python
from terminarty import Box, BoxStyles

print(Box("Hello World", BoxStyles.Ascii))
```

There are several box styles available:

```text
Ascii:
    +───────────+
    │Hello World│
    +───────────+
Thin:
    ┌───────────┐
    │Hello World│
    └───────────┘
Thick:
    ┏━━━━━━━━━━━┓
    ┃Hello World┃
    ┗━━━━━━━━━━━┛
Double:
    ╔═══════════╗
    ║Hello World║
    ╚═══════════╝
Round:
    ╭───────────╮
    │Hello World│
    ╰───────────╯
```

**Waitings**

```python
from terminarty import Waiting
import time

with Waiting("Loading"):  # "Loading..." would work the same
    time.sleep(5)
```

!["Loading..."](https://media.giphy.com/media/qFxscRiUabzl0p5twq/giphy.gif)

**Progress Bars**

```python
from terminarty import ProgressBar
import time

progress = ProgressBar(121)
for _ in range(121):
    time.sleep(0.1)
    progress += 1
```

!["Progress Bar"](https://media.giphy.com/media/GT8mIvDlXOdnyLdKyr/giphy.gif)
> **Note**
> If you want to print something while the waiting or progress bar is running,
> you would need to use ``terminal.print()`` instead of ``print()``