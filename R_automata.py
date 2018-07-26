import numpy as np

class R_Automata(object):

    def __init__(self, nbL=0, nbS=0, initial=[], final=[], transitions=[]):
        """
        Constructor of R automaton
        """
        self.nbL = nbL
        self.nbS = nbS
        self.initial = initial
        self.final = final
        self.transitions = transitions

    def generate(self):
        pass

    """
    Forward algorithm in "Representing Distributions over Strings with
                          Automata and Grammars", Page 105
    """
    def parse(self, string):
        #Algorithm 5.2: FORWARD.
        n = int(len(string))
        Q = self.nbS
        F = np.zeros((n+1, Q), dtype=np.float64)
        
        #initialize
        for j in range(0,Q):
            F[0][j] = self.initial[j]

        for i in range(1,n+1):
            for j in range(0,Q):
                index = string[i-1]
                F[i][j] += F[i-1]@ex_transitions[index][:, j]

        #Algorithm 5.3: Computing the probability of a string with FORWARD.
        T = 0
        for j in range(0,Q):
            T += F[n][j]*self.final[j]
            print(F)
        return T
            

# a@b
"""
Input Examples from http://pageperso.lif.univ-mrs.fr/~remi.eyraud/scikit-splearn/ 
"""
ex_initial = np.array([1, 0], dtype=np.float64)
ex_final = np.array([0, 1/4], dtype=np.float64)

ex_transitions = {
    'a': np.array([[1/2, 1/6],
                    [0,  1/4]], dtype=np.float64),
    'b': np.array([[0,   1/3],
                    [1/4, 1/4]], dtype=np.float64)
}

ex_automaton = R_Automata(2,2,ex_initial, ex_final, ex_transitions)
print('generate a string:', ex_automaton.generate())
print('probability of "aba":',ex_automaton.parse('aba'))
