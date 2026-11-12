# CarLearnDrive
### A visual experiment in neuroevolution

CarLearnDrive is a Python simulation in which a population of cars navigates a 2D track. Each car uses a small neural network to decide how to accelerate and steer. A custom genetic algorithm evolves the network weights between generations.

The project brings together simulation, simple vehicle physics, ray-casting sensors, and evolutionary optimization in an interactive Pygame window.

## Features

- Three selectable tracks, including a narrow zigzag layout.
- Five distance sensors per car.
- A 5-input, 6-hidden-unit, 2-output neural network implemented with NumPy.
- Adjustable population size, mutation rate, and generation limit.
- Elite selection, uniform crossover, and Gaussian mutation.
- Obstacles introduced during each generation.
- On-screen generation, driving, finishing, and obstacle statistics.

**Built with:** Python, pygame-ce, NumPy. The evolution logic is implemented in `evolution.py`; it does not use NEAT.

## Run locally

You need Python 3 and a desktop environment capable of opening a Pygame window.

```bash
git clone https://github.com/Larosy/CarLearnDrive.git
cd CarLearnDrive
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and start the simulation:

```bash
python -m pip install -r requirement.txt
python main.py
```

The dependency file is named `requirement.txt` in this repository.

## Controls

| Screen | Controls |
| --- | --- |
| Welcome | Enter to continue |
| Evolution settings | Up/Down selects a setting; Left/Right changes its value; Enter confirms |
| Track selection | Up/Down selects a track; Enter starts the simulation |
| Simulation | Close the window to exit |
| Results | Escape or close the window to exit |

## How the cars improve

Each car receives five normalized sensor distances and produces acceleration and steering outputs. Cars gain fitness by moving, with a penalty for excessive steering and collisions, plus a reward for reaching the finish condition.

At the end of a generation, the best-performing cars supply the next population's weights. The algorithm preserves elites and creates the remaining cars through crossover and mutation.

## Code map

| File | Responsibility |
| --- | --- |
| `main.py` | Menus, track generation, obstacles, rendering, and simulation loop |
| `car.py` | Vehicle motion, sensors, collision detection, and fitness |
| `network.py` | Feedforward neural network and weight serialization |
| `evolution.py` | Selection, crossover, mutation, and population management |

## Experiment notes

This is a learning simulation, not a real-world autonomous-driving system. Outcomes vary between runs because initialization, mutation, and obstacle placement are random. The stopping condition may be the generation limit rather than every car finishing.

Possible extensions include reproducible random seeds, saving the best network, comparing fitness curves, and recording runs across different tracks.

## Author

[Ozan Honça](https://www.linkedin.com/in/ozan-honca/) · [GitHub](https://github.com/Larosy)
