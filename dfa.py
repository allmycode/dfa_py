class CharClass:
    def __init__(self, func):
        self.func = func

    def __call__(self, c):
        return self.func(c)

def frset(*s):
    return frozenset(s)

def joined(*args):
    def check(c):
        for f in args:
            if callable(f) and f(c): return True
            if isinstance(f, frozenset) and c in f: return True
        return False
    return CharClass(check)


CC_LETTER = CharClass(str.isalpha)
CC_DIGIT  = CharClass(str.isdigit)
CC_SPACE  = frset(' ', '\t', '\n')
CC_ID_S = joined(CC_LETTER, frset('-', '_'))
CC_ID_B = joined(CC_ID_S, CC_DIGIT, frset('.'))

def istuple(t): return isinstance(t, tuple)        

class DFAContext:
    def __init__(self, a):
        self.a = a
        self.stack = []

    def process(self, i, c):
        for s in self.stack:
            s(i, c)

    def push(self, s):
        self.stack.append(s)
    
    def pop(self):
        return self.stack.pop()

    def transit_to(self, s, index, c):
        newstate = s
        if istuple(s):
            newstate = s[0]
            accumulator = s[1]
            self.push(accumulator)

        self.notify(index, c, newstate)
        return newstate

    def notify(self, index, c, state):
        for acc in self.stack:
            if not acc(index, c, state):
                self.pop()

    def process(self, index, c, state):
        m = self.a.get(state);
        if m:
            if m.get(c):
                return self.transit_to(m.get(c), index, c);
            else:
                for f in filter(callable, m.keys()):
                    if f(c): return self.transit_to(m[f], index, c)
                for s in filter(lambda k: isinstance(k, frozenset), m.keys()):
                    if c in s: return self.transit_to(m[s], index, c)
                
        else:
            return None    












if __name__ == "__main__":
    import sys
    
    def no1(c): return c != '1'
    tr = {
        1: {'1': (2, "at two")},
        2: {'1': 3},
        3: {no1: 3, '1': 4},
        4: {'0': 3, '1': 5},
        5: {'0': 3, '1': 5}
    }

    s = 1;
    for c in sys.argv[1]:
        rs = sigma3(tr, c, s);
        print(str(s) + "->" + str(rs) + " by '" + c + "'")
        s = rs
        if s == None:
            print("invalida transition. Failed")
            break
    
    if s == 5:
        print("Finished")
    else:
        print("Not in final state. Failed")
