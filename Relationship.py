class Relationship:

    def __init__(self, type, sign, source, target):
        self.type = type
        self.sign = sign
        self.source = source
        self.target = target

    def printSelf(self):
        print("*"*100)
        print("type: ", self.type)
        print("sign: ", self.sign)
        print("source: ", self.source)
        print("target: ", self.target)

