import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(open('words.utf-8.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    #print('candidates: '+NWORDS.get)
    likelyCandidate = max(candidates, key=NWORDS.get)
    return likelyCandidate

def filterAndCorrect(word):
    data = open("words.utf-8.txt")
    corrected = correct(word)
    for line in data:
        if corrected+'\n' == line:
            #print (word + ' corrected to ' + corrected)
            return corrected
    #print (word + ' not corrected ')
    return ''

def filterAndCorrectString(string):
    splitString = string.split(' ')
    processedString = ''
    for x in splitString:
        processedString += filterAndCorrect(x) + ' '
    return processedString
def filterAndCorrectStringIntoFile(string, file):
    print('Spell checking \''+string+'\'...')
    file.write(filterAndCorrectString(string))
def filterAndCorrectFile(filename):
    print("Opening "+filename+"...")
    processed = open ("Spell_Checked_"+filename, 'a')
    with open (filename, "r") as myfile:
        data=myfile.read().replace('\n', ' ')
    print('Spell checking '+filename+' into Spell_Checked'+filename+"...")
    filterAndCorrectStringIntoFile(data, processed)
    processed.close()
#run spell checker for all reviews in our scope removing words which spelling cannot be found
#print(filterAndCorrectString('helllo worl hiw are yuo http://website.com'))

open('Spell_Checked_S1.txt')
i = 1
while i <= 5:
    filterAndCorrectFile('S'+str(i)+'.txt')
    i = i + 1
#print(correct('worl'))
#print(filterAndCorrectFile('words.utf-8.txt'))