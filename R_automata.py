import numpy as np

from numpy.linalg import inv

import math

from DS import Queue

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
        self.alphabet = self.transitions.keys()

    """
    Forward algorithm in "Representing Distributions over Strings with
                          Automata and Grammars", Page 105
    """
    def parse(self, string):
        #Algorithm 5.2: FORWARD.
        n = int(len(string))
        Q = self.nbS
        F = np.zeros((n+1, Q), dtype=np.float64) #F[n][s] = Pr_A(x,q_s), string x = a_1 a_2 ... a_n

        #initialize
        F[0] = self.initial

        for i in range(1,n+1):
            key = string[i-1]
            F[i] += F[i-1]@self.transitions[key][:,:]

        #Algorithm 5.3: Computing the probability of a string with FORWARD.
        T = F[n]@np.transpose(self.final)

        return T


# a@b

class PFA(R_Automata):
    def __init__(self, nbL=0, nbS=0, initial=[], final=[], transitions=[]):
        super(PFA, self).__init__(nbL, nbS, initial, final, transitions)

    def probability_cond(self):
        if abs(np.sum(self.initial), 1.0) > 1e-8:
            return False, "Wrong initial prob"
        for q in range(self.nbS):
            total_prob = .0
            for _, transition in self.transitions.items():
                total_prob += transition[q,:].sum()
            total_prob += self.final[q]
            if abs(total_prob, 1.0) > 1e-8:
                return False, "Wrong transition prob at state %d"%(q)
        return True, ""

    def halting_cond(self):
        pass

    def generate(self):
        s = np.random.choice(self.nbS, p=self.initial)
        generated = ""
        while True:
            # P(x) = sum_E P(x|E)p(E)
            # get an alphabet
            a = np.random.choice(self.nbL + 1,
                                 p=[pr_a[s].sum() for pr_a in self.transitions.values()] + [self.final[s]])
            if a == self.nbL:
                return generated
            else:
                generated += a

            # get the next state
            s = np.random.choice(self.nbS,
                                 p=self.transitions[a][s])
        return generated


    def prefix_prob(self, w):
        """
        Input           a PFA, a string w
        Output          the probability of w appearing as a prefix
        Author          Yu-Min Kim
        """

        result = self.initial
        
        for char in w:
            result = result @ self.transitions[char]

        return result.sum()

    def prefix_prob2(self, w):

        M = np.zeros((self.nbS, self.nbS))
        for _, matrix in self.transitions.items():
            M += matrix

        I = np.eye(self.nbS)

        M_w = np.eye(self.nbS)
        for char in w:
            M_w= M_w @ self.transitions[char]

        return self.initial @ M_w @ inv(I - M) @ self.final

    def suffix_prob(self, w):
        """
        Input           a PFA, a string w
        Output          the probability of w appearing as a suffix
        Author          Yu-Min Kim
        """

        M = np.zeros((self.nbS, self.nbS))
        for _, matrix in self.transitions.items():
            M += matrix

        I = np.eye(self.nbS)

        M_w = np.eye(self.nbS)
        for char in w:
            M_w= M_w @ self.transitions[char]

        return self.initial @ inv(I - M) @ M_w @ self.final

    def BMPS_exact(self, p):
        """
        Algorithm 2 in sampling-algorithm.pdf
        
        Input           a PFA, p >= 0
        Output          the string w such that PrA(w) > p or false if there is no such w
        Description     Solve the decision problem BMPS(Bounded Most Probable String)
                        which returns the string whose probability is greater than p and
                        length is less than b.
        Complexity      O((b * nbL * (nbs**2)) / p) if all operations are constant

        Author          Yu-Min Kim
        """

        def calculate_b(p):
            """
            b is the bound parameter which constraints the length of the string w.
            This function calculates the value of b.
            """
            M = np.zeros((self.nbS, self.nbS))
            for _, matrix in self.transitions.items():
                M += matrix
            
            I = np.eye(self.nbS)

            u = self.initial @ M @ (inv(I - M) ** 2) @ self.final

            var = self.initial @ M @ (I + M) @ (inv(I - M) ** 3) @ self.final \
                        - ( self.initial @ M @ (inv(I - M) ** 2) @ self.final ) ** 2 

            return  math.ceil(u + var / p)

        # Calculate bound
        b = calculate_b(p)
        #print('b value', b)

        # Initially, the result string is empty string (lambda)
        w = ''

        # Instantiate a Queue
        Q = Queue()

        # The probability of lambda string
        p_0 = self.initial @ self.final
        
        # If the probability of lambda stirng is larger than p, then return it.
        if p_0 > p:
            return w
        
        # Enqueue the probability of the lambda string
        Q.enqueue((w, self.initial))

        while not Q.is_empty():
            # w is string and V is a matrix
            w, V = Q.dequeue().data
            print('current string', w)

            for char in self.alphabet:
                #print('alphabet', char)
                V_new = V @ self.transitions[char]

                if V_new @ self.final > p:
                    return w + char

                if len(w) < b and V_new.sum() > p:
                    #print('Enqueue!', w + char)
                    Q.enqueue((w + char, V_new))
        
        return False




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

ex_automaton = PFA(2,2,ex_initial, ex_final, ex_transitions)
#print('generate a string:', ex_automaton.generate())
print('probability of "aba":',ex_automaton.parse('aba'))
print('most probable string: ', ex_automaton.BMPS_exact(0.1))
print('prefix_prob of "aba":', ex_automaton.prefix_prob('aba'))
print('prefix_prob2 of "aba":', ex_automaton.prefix_prob2('aba'))
print('suffix_prob of "aba":', ex_automaton.suffix_prob('aba'))