__author__ = 'yuranich'

myId = 45079007
apiVersion = 5.33

fields = ['city',
          'country',
          'universities',
          'schools',
          'occupation',
          'personal',
]

rusId = 98411123
olegId = 12587306
alenaId = 59070494
vladId = 71767930

def getToken(name):
    tokens = dict(line.strip().split('=') for line in open('tokens.txt'))
    return tokens[name]