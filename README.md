# To-Do List App

Final project submission by Emirhan Uçan

---

A simple to-do list app I built using Python and PyQt6. You can add tasks, check them off when done, and delete them. It also saves your tasks so they don't disappear when you close the app.

## What you need

- Python 3.10 or newer
- PyQt6

## How to run

Install the dependencies first:
```
pip install -r requirements.txt
```

Then just run:
```
python main.py
```

## Running with Docker

Build the image:
```
docker build -t todo-app .
```

Run it (Linux/Mac):
```
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix todo-app
```

## Files

- `main.py` — the app itself
- `requirements.txt` — dependencies
- `Dockerfile` — for running in a container
