# wordle
A Python bot that (naively) plays the game Wordle.


## Usage
Clone repo and navigate to folder. Make sure to install all requirements first:
```python
pip install -r requirements.txt
```
To import:
```python
from wordle import Wordle
```

### Initialization
To initialize:
```python
w = Wordle()
```
In this case, a new Wordle object is created, and a random word is chosen as the answer for the bot to attempt to guess. The random word is chosen by default from NYT's list of possible answers, and the guesses are by default chosen from NYT's list of possible words.

To have the bot play with an answer of your choice, you can initialize as follows:
```python
w = Wordle(answer=your_answer)
```

To have the bot play with the list of words from the old Wordle site, you can add another parameter as follows:
```python
w = Wordle(version='old')
```
The parameter *version* must be either 'new' or 'old'.

### Playing
To have the bot play a game:
```python
w.play()
```
The bot will play a game, making guesses until it fails or correctly guesses the word. The state of the final board will be printed to the console.
The bot plays differently each time you call play().

You can also simulate 100 plays for a given word:
```python
w.simulate()
```
OR simulate as many plays as you like:
```python
w.simulate(1000)
```

## Misc
Feel free to clone and make your own changes/analyses! Interestingly, a bot as naive as this one still wins about 95% of the time. Maybe you can add features to make it even better!
