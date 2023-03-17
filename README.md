# RollPy
**Python module to handle discrete random variables**
(or *Will That Die Roll Kill Me?*)

Are you looking to crunch some probabilities on dice outcomes, or simply make informed decisions to design the best strategy for crushing your ennemies in role-playing? ⚔️ Look no further: this library got you covered! 🎲

## How to use?
Everything starts with a die roll...
```
from rollpy import Roll
roll = Roll(20) # d20 roll
```

Random variables are handled as events. Define an Event as the result of some function on a list of some other event outcomes
```
from rollpy import Roll, Event
my_rolls = [Roll(6)]*3 + [Roll(8)]*2 # rolling 3d6 + 2d8

def success(rolls):
    sum_roll = sum(rolls)
    return(sum_roll > 29)

succeeded = Event(success, my_rolls)
succeeded.show()
```
> P(False) = 761/768
>
> P(True) = 7/768

As you can see, probabilities are given as exact fractions whenever possible!

## Handling lots, lots of dice? 🎲<sup>lots</sup>
*Coming soon...*

## How does it work?
Discrete random variables are handled as pairs of (outcome, probabilty) and updated accordingly.
