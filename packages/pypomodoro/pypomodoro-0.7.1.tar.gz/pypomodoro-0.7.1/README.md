# PyPomodoro

Displays a full screen [Pomodoo](https://en.wikipedia.org/wiki/Pomodoro_Technique) timer in your terminal. 

## Installation

```bash
pip install pypomodoro
```

## Screenshot

![Screenshot](screenshot.png)

## Usage

```
pypomodoro [-h] [-w WORK_MINS] [-b BREAK_MINS] [-v] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -w WORK_MINS, --work WORK_MINS
                        Number of miinutes for work
  -b BREAK_MINS, --break BREAK_MINS
                        Number of minutes for break
  -v, --verbose         Move detailed display
  --version             show program's version number and exit
```

## Development

Create virtual env and install dev dependencies
```bash
make init
```
Run tests in venv
```bash
make test
```
Run the app in venv
```bash
make run
```