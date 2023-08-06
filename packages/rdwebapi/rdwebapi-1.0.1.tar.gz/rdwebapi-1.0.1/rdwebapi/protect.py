_varTag_ = 1
_varTitle = 'private'
def getTag():
    print(_varTag_)

def getTitle():
    print(_varTitle)

def _getTitle():
    print(_varTitle)

class Protect():
    def getTitle(self):
        print(_varTitle)

    def _getTitle(self):
        print(_varTitle)