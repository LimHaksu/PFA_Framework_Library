import numpy as np
class DFA:
    def __init__(self, nbL = 0, nbS = 0, initial_state = 0, states = [], transitions = {}, final_states = []):
        self.nbL = nbL
        self.nbS = nbS
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.alphabets = []
        """
        transitions input : sparse matices -> {(current_state, alphabet), next_state}
        """
        self.transitions = {} # key : (current_state, alphabet), value : next_state
        for alphabet in transitions:
            self.alphabets.append(alphabet)
            for current_state in range(transitions[alphabet].shape[0]):
                if(np.count_nonzero(transitions[alphabet][current_state]) > 1):
                    None
                    #raise InvalidDFA
                next_state = np.where(transitions[alphabet][current_state] == 1)[0][0]
                self.transitions[(current_state,alphabet)] = next_state 
        self.final_states = final_states

        """
        transitions input : {(current_state, alphabet), next_state}
        """
        """
        self.transitions = transitions
        """
    def verify_acceptance(self, string):
        current_state = self.initial_state
        for alphabet in string:
            if alphabet not in self.alphabets:
                return False
            current_state = self.transitions[(current_state,alphabet)]
        if current_state in final_states:
            return True
        else:
            return False
    
if __name__ == "__main__":
    nbL = 2
    nbS = 5
    initial_state = 0
    transitions = {'a' : np.array([[0,1,0],
                                   [0,0,1],
                                   [0,0,1]],dtype = np.float64),
                   'b' : np.array([[0,0,1],
                                   [0,1,0],
                                   [0,0,1]],dtype = np.float64)}
    states = [0,1,2]
    final_states = [2]
    dfa = DFA(nbL, nbS, initial_state, states, transitions, final_states)
    print(dfa.transitions)