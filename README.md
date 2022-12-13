# Pong AI
### An rallying AI that plays Pong
##### By Sam Reiter, Adie Guo, and Sam Robinson


![](https://media.giphy.com/media/HQlb1YUv0GtmyEVCqy/giphy.gif)

[Full video](https://drive.google.com/file/d/1jogvmUo2OPmf_dEu7pDzd8V9-vyO_2n_/view?usp=sharing)



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
With pacman:
```bash
sudo pacman -S python-numpy python-pandas python-matplotlib python-pygame
```
With conda
'''bash
conda install --Dependencies
'''



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

##### agent.py
Our RL agent which interacts with the game
##### functions.py
Contains our loss function and  activation functions
##### layers.py
Layers of our model
##### network.py
Our network of layers
##### pong.py
Code for the game pong
##### train.py

## References Used
This project was coded without machine learning libraries. Here is a playlist of videos used to achieve this.

[![AI VIDEOS](https://i.ytimg.com/vi/IHZwWFHWa-w/maxresdefault.jpg)](https://youtube.com/playlist?list=PLKM3Q3j59zpH7O0VQGFCvmW5ISlM0tys6)

## Next Steps
- make the bias work
- train after each move rather than each game
- Integrate a proper reinforcement-learning algorithm.
- Add a second AI to play against the first.
- Use GPU acceleration.
- Create binaries for different OSs so dependencies aren't needed
