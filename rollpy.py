from itertools import product
from math import prod
from fractions import Fraction

class Event(object):
    def __init__(self, f=None, args=None, results=None, verbose=True):
        self.verbose = verbose
        if results is None:
            self.f = f
            self.args = args
            self._run()
        else:
            self.results = results
        self.outcomes = tuple(self.results.keys())
        self.probabilities = tuple(self.results[key] for key in self.outcomes)
    
    def _run(self):
        self._combinations = prod([len(arg.outcomes) for arg in self.args])
        # Run all combinations
        self.results = dict()
        all_inputs = product(*[arg.outcomes for arg in self.args])
        all_probas = product(*[arg.probabilities for arg in self.args])
        for iter_num, (inputs, probas) in enumerate(zip(all_inputs, all_probas)):
            outcome = self.f(inputs)
            self.results[outcome] = prod(probas) + self.results.get(outcome, 0)
            if self.verbose:
              print(f'{(iter_num+1)/self._combinations:.3%}', end='\r')
    
    def show(self):
        for val, p in zip(self.outcomes, self.probabilities):
            print(f'P({val}) = {p} ~ {float(p):.2%}')

class Roll(Event):
    def __init__(self, k):
        outcomes = [i+1 for i in range(k)]
        p = Fraction(1, k)
        results = dict([(outcome, p) for outcome in outcomes])
        super().__init__(results=results)
