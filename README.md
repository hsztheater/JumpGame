# **Jump Game**
A simple game made with pygame zero

Nothing fancy, my first endless runner type game using pygame zero. The code is a mess and need improvement.

**MAIN ISSUES:**

When the player wins and press space to go back to the main menu, the main menu opens for a fraction of a second and doesn't wait for the second "space" input before starting the game. I tried to add a timer calling another function like so:

```python
def menu():
  clock.schedule(mainmenu,2)
```

```python
def mainmenu():
  global STARTED
  STARTED = True
```
  
It sort of fixes the problem but in some occurences, it starts the game for a fraction of a second, then goes back to the main menu again, and I have to press space several times to fix it and start a game again.

Another issue is that the game doesn't seem to restart properly after a win or a gameover. It is possible to retry but it seems that the state of the game resumes from how it was when you lost or won.
