# Pong AI
### An rallying AI that plays Pong
##### By Sam Reiter, Adie Guo, and Sam Robinson


## Dependencies
- Python
- numpy
- pandas
- matplotlib
- pygame
##### To install:
With pip:
```bash
python -m pip install numpy pandas matplotlib pygame
```
pacman:
```bash
sudo pacman -S python-numpy python-pandas python-matplotlib python-pygame
```

## Usage
##### Run
```bash
python train.py
```

##### If you\'d like to play pong by yourself run
```bash
python pong.py
```
## File Descr.

####agent.py
Our RL agent which interacts with the game
####functions.py
Contains our loss function and  activation functions
####layers.py
Layers of our model
####network.py
Our network of layers
####pong.py
Code for the game pong
####train.py

##References Used
This project was coded without machine learning libraries. Here are some resources used to achieve this.

<p align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?list=PLKM3Q3j59zpH7O0VQGFCvmW5ISlM0tys6" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</p>

## Next Steps
- Integrate a proper reinforcement-learning algorithm.
- Add a second AI to play against the first.
- Use GPU acceleration.
- Create binaries for different OSs so dependencies aren't needed
