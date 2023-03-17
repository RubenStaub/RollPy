from itertools import product
from math import prod
from fractions import Fraction

class Event(object):
    def __init__(self, f=None, args=None, results=None, verbose=True, keep_tree=False):
        self.verbose = verbose
        if keep_tree:
            self.f = f
            self.args = args
        if results is not None:
            self.results = results
        else:
            self.results = dict()
            if isinstance(args, Event):
                args = (args,)
                func = lambda x: f(*x)
            else:
                func = f
            self._run(func, args)
        self.outcomes = tuple(self.results.keys())
        self.probabilities = tuple(self.results[key] for key in self.outcomes)
    
    def _run(self, f, events):
        self._combinations = prod([len(event.outcomes) for event in events])
        # Run all combinations
        all_inputs = product(*[event.outcomes for event in events])
        all_probas = product(*[event.probabilities for event in events])
        for i, (inputs, probas) in enumerate(zip(all_inputs, all_probas)):
            outcome = f(inputs)
            self.results[outcome] = prod(probas) + self.results.get(outcome, 0)
            if self.verbose:
              print(f'{(i+1)/self._combinations:.3%}', end='\r')
    
    def show(self):
        for val, p in zip(self.outcomes, self.probabilities):
            print(f'P({val}) = {p} ~ {float(p):.2%}')

class Roll(Event):
    def __init__(self, k):
        outcomes = [i+1 for i in range(k)]
        p = Fraction(1, k)
        results = dict([(outcome, p) for outcome in outcomes])
        super().__init__(results=results)

def reduce(f, events, verbose=True):
    # Initialize reduce
    reduce_event = events[0]
    # Run reduce iteratively
    for i, event in enumerate(events[1:]):
        if verbose:
            print(f'Processing reduce {i+1}/{len(events)-1}')
        reduce_event = Event(f, (reduce_event, event))
    return reduce_event
