DSA Project - Simulating Epidemics
==================================

### Project Details.

<!-- DESCRIPTION -->

**Group members:**
+ Azka Amer
+ Rashid Talha
+ Zeenia Asr

### Usage.

**Installation:**

The code is written entirely in python. All the dependencies can be install using pip.
```
pip install -r requirements.txt
```

**Running the simulation:**

Simulation parameters can be set within `main.py`. Further thresholds can be controlled by inheriting the base classes VirusBase and AgentBase, and overwriting their class variables. The simulation itself is run by calling the `main.py` file

```
python main.py
```

By default a live simulation is played. The user can alternatively save it to the file by passing `save_to_disk=True` as an argument to the `run_simulation` function inside the main script.

