from dfa import *

class TagNameAccumulator:
    def __init__(self):
        self.name = ""

    def __call__(self, index, c, state):
        if state == 5:
            self.name += c
            return True
        else:
            print ("Tag: " + self.name)
            self.name = ""
            return False

class XmlTagAccumulator:
    def __init__(self):
        self.tag = ""

    def __call__(self, index, c, state):
        if state != 1:
            self.tag += c
            return True
        else:
            self.tag += c
            print ("XML Tag: " + self.tag)
            self.tag = ""
            return False

tagname = TagNameAccumulator()
xmltag = XmlTagAccumulator()

LT = '<'
GT = '>'
a = {
    1: {CC_SPACE: 2, LT: (3, xmltag)},
    2: {CC_SPACE: 2, LT: (3, xmltag)},
    3: {CC_SPACE: 4, CC_ID_S: (5, tagname)},
    4: {CC_SPACE: 4, CC_ID_S: (5, tagname)},
    5: {CC_ID_B: 5, CC_SPACE: 6, GT: 1},
    6: {CC_SPACE: 6, GT: 1}
}
import sys
s = 1;
z = DFAContext(a)
for i, c in enumerate(sys.argv[1]):
    rs = z.process(i, c, s);
    print(str(s) + "->" + str(rs) + " by '" + c + "'")
    s = rs
    if s == None:
        print("invalida transition. Failed")
        break

if s == 1:
    print("OK")
else:
    print("Incorrect finish state " + str(s))
            
