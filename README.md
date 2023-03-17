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

Random variables are handled as events. Define an Event as the result of some function on some other event outcomes
```
from rollpy import Roll, Event
my_rolls = [Roll(6)]*3 + [Roll(8)]*2 # rolling 3d6 + 2d8

def success(rolls):
    sum_roll = sum(rolls)
    return(sum_roll > 29)

succeeded = Event(success, my_rolls)
succeeded.show()
```
> P(False) = 761/768\
> P(True) = 7/768

As you can see, probabilities are given as exact fractions whenever possible!

### More examples
Similarly, it's easy to count whatever you want as well:
```
from rollpy import Roll, Event
from math import factorial

def is_prime(x): # Wilson's theorem
    return factorial(x-1) % x == x-1

def count_nb_primes(rolls):
    return sum(is_prime(roll) for roll in rolls)

rolls = [Roll(6)]*10 # rolling 10d6

Event(count_nb_primes, rolls).show()
```

Which is equivalent to the much faster code:
```
from rollpy import Roll, Event
from math import factorial

def is_prime(x): # Wilson's theorem
    return factorial(x-1) % x == x-1

roll_prime = Event(is_prime, Roll(6))

Event(sum, [roll_prime]*10).show()
```

For fast operations, try to avoid combining lots of events with many outcomes each. Here, we first reduce the 6 outcomes of a d6 into 2 outcomes (prime or not) with according probabilities.

## Handling lots, lots of dice? 🎲<sup>🎲</sup>
Large amount of dice can be handled with the `rollpy.reduce` function, which performs the reduce function sequentially.

For example, the probability that the sum of a 100d8 roll is prime:
```
from rollpy import Roll, Event, reduce
from math import factorial

def is_prime(x): # Wilson's theorem
    return factorial(x-1) % x == x-1

my_rolls = [Roll(8)]*100 # rolling 100d8

sum_rolls = reduce(sum, my_rolls)

Event(is_prime, sum_rolls).show()
```
> P(False) = [...exact fraction...] ~ 82.26%\
> P(True) = [...exact fraction...] ~ 17.74%

If you can compute this, you can compute (almost) everything 😉 ...such as the number of pairs of 10 after a 20d10 roll:
```
from rollpy import Roll, Event, reduce

roll_10 = Event(lambda x: x==10, Roll(10)) # Event for 1d10 rolled 10 (or not)

Event(lambda rolls: sum(rolls)//2, [roll_10]*20).show()
```

## How does it work?
Discrete random variables are handled as pairs of (outcome, probabilty) and updated accordingly.

The reduce function `reduce(f, [event1, event2, event3, ...])` is a helper for:
`Event(f, [Event(f, [Event(f, [event1, event2]), event3]), ...])`.\
So the `f` function will be used as `f(f(f(o1, o2), o3), ...)`
