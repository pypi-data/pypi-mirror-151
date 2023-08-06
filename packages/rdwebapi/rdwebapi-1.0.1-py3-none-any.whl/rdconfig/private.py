__varName__ = 1
__varCaption = 'private'
def getName():
    print(__varName__)

def getCaption():
    print(__varCaption)

def __getCaption():
    print(__varCaption)

class Private():
    def __getCaption(self):
        print(__varCaption)

    def getName(self):
        print(__varName__)

