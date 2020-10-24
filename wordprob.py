# CS1210 HW2
#
# I certify that this file contains only my own work. I also certify
# that I have not shared the contents of this file with anyone in 
# any form.

from statistics import mean
from math import sqrt

######################################################################
# Specification: opens file and reads the text, returning the entire
# text as a string.
#
def getText(file):
    '''Reads in a file and returns it as one, readable string.'''
    # Opens the text file.
    infile = open(file, 'r')
    
    # Creates a list containing each line in the file.
    T = infile.readlines()
    
    # Iterates through T and turns all blank lines and CAPS lines into empty 
    # strings.
    for line in range(len(T)):
        if T[line].upper() == T[line]:
            T[line] = ''
            
    # Concatenates T into one string and replaces newline characters with
    # spaces and removes newline characters that are preceded by a hyphon
    # along with the hyphon.
    F = ''.join(T).replace('-\n', '').replace('\n', ' ')

    infile.close()
    
    # An unwanted space will be present at the end of F if the last "readable"
    # line used to be followed by a blank or CAPS line(s) in the original file.
    # The following statement checks if this is the case and returns the
    # correct string.
    if( F[-1] == ' ' ):
        return F[:-1]
    return F

######################################################################
# Specification: takes a string, text, and removes possessives ('s)
# and most punctuation ('(),:\'"-—_'). 
#
def flushMarks(text):
    '''Takes a string and removes most punctuation, possessives, and
    replaces sentence-ending punctuation with periods.'''
    
    # Any of the three lists, period, space, or remove, below can be altered
    # to add more punctuation changes.
    
    # List containing punctuation that needs to be changed to a period.
    period = ['!', '?', ';']
    
    # List containing punctuation that needs to be changed to a space.
    space = ['--', '-', '_']
    
    # List containing punctuation that needs to be removed.
    remove = ["'s", '...', '(', ')', ',', ':', "'", '"']
    
    # Iterates through period, replacing punctuations with periods.
    for i in range(len(period)):
        text = text.replace(period[i], '.')
        
    # Iterates through space, replacing punctuations with periods.
    for i in range(len(space)):
        text = text.replace(space[i], ' ')
        
    # Iterates through remove, removing punctuations.
    for i in range(len(remove)):
        text = text.replace(remove[i], '')
        
    return text
    
######################################################################
# Specification: returns a list of k words starting at word i of the
# text. 
#
def extractWords(text, i=0, k=None):
    '''Returns a list of k words starting at word i of a text.'''
    # Creates a list of each word in text in lowercase; uses flushMarks()
    # to remove punctuation and removes the periods left over.
    W = [ j for j in flushMarks(text).lower().replace('.', '').split() ]
    
    return W[i: i+k]

######################################################################
# Specification: returns a list of sentences starting at word i
# of the text. 
#
def extractSentences(text, i=0, k=None):
    '''Returns a list of the sentences starting from word i and ending at word
    i+k in the text. Periods are also removed.'''
    # Keeps track of which sentence is being formed.
    count = 0
    
    # List of all the words in text, including periods.
    W = [ r for r in flushMarks(text).split() ]
    
    # A list which will contain the sentences we want. Has k elements to ensure
    # that the list is large enough.
    S = ['']*k
    
    # Iterates through the list of words, W, from i to i+k.
    for j in range(i, i+k):
        
        # If i+k is greater than or equal to the length of the list of words,
        # W, this breaks out of the loop.
        if (j >= len(W)):
            break
        
        # When W[j] is the end of a sentence, it is added to its respective
        # sentence. Count is then increased so that future words are added to
        # a new sentence as well as the period being removed.
        if '.' in W[j]:
            S[count] += ' ' + W[j]
            S[count] = S[count].replace('.', '')
            count += 1
            
        # Adds a word to a sentence.
        else:
            S[count] += ' ' + W[j]
    
    # Removes spaces from the beggining of each element in S and ignores
    # the leftover empty strings in S. Then returns the list of sentences.
    sentences = [r.strip() for r in S if len(r) > 0]
    return sentences

######################################################################
# Specification: returns an integer denoting the number of syllables
# in the specified word.
#
# Syllables are defined according to a few simple rules:
#   1. flush trailing -s and -e
#   2. each syllable starts with a vowel
#   3. y is a vowel when it follows a consonant
#   4. every word has at least one syllable
#
def countSyllables(word):
    '''Returns an integer count of the number of syllables in word.'''
    # Figure effective length of the word.
    length = len(word)
    # Flush trailing -s and -e
    if word[-1]=='s' or word[-1]=='e':
        length = length-1
    # Consume any leading consonants.
    i = 0
    while i < length and word[i].lower() not in 'aeiouy':
        i = i+1
    # Start counting syllables, starting with the first vowel (or y,
    # which is a vowel when it follows a consonant).
    s = 0
    while i < length:
        # New syllable.
        s = s+1
        # Consume a leading y, if present.
        if word[i].lower() == 'y':
            i = i+1
        # Consume characters while there are more vowels; here, a y is
        # a consonant.
        while i < length and word[i].lower() in 'aeiou':
            i = i+1
        # Consume cluster of consonants if there is any word left,
        # stopping at first vowel or y. Must consume at least one
        # consonant to consider y a vowel again.
        if i < length:
            i = i+1   # A non-y consonant.
        while i < length and word[i].lower() not in 'aeiouy':
            i = i+1
    # Every word has at least one syllable.
    return(max(s,1))

######################################################################
# Lasbarhetsindex Swedish Readability Formula
#   http://www.readabilityformulas.com/the-LIX-readability-formula.php
# wrd is the number of words
# lng is the number of long words (> 6 characters)
# snt is the number of sentences
# LIX = wrd/snt + (lng*100)/wrd
#
# Returns a floating point value.
#
def lix(text, i=0, k=None):
    '''Calculates the LIX of a text.'''
    # Number of words in text.
    wrd = len(extractWords(text, i, k))
    
    # Number of words with a length greater than 6 in text.
    lng = len( [ l for l in extractWords(text, i, k) if len(l) > 6 ] )
    
    # Number of sentences in text.
    snt = len(extractSentences(text, i, k))
    
    # Calculation of LIX.
    return wrd/snt + (lng*100)/wrd

######################################################################
# Gunning's Fog Index:
#   http://www.readabilityformulas.com/gunning-fog-readability-formula.php
# asl is the average sentence length
# phw is the percent of "hard" words, where "hard" means 3 or more syllables
# FOG = 0.4(asl + phw)
#
# Returns a floating point value.
#
def fog(text, i=0, k=None, csyl = countSyllables):
    '''Calculates the Fog index of a text.'''
    # Calculates the average sentence length.
    asl = mean( [ len(extractSentences(text, i, k)[j].split()) for j in \
                 range(len(extractSentences(text, i, k))) ] )
    
    # Calculates the percentage of words with 3 or more syllables.
    phw = 100 * len([w for w in extractWords(text, i, k) if csyl(w) >= 3]) \
        / len(extractWords(text, i, k))
        
    # Calculates the Fog index.
    return 0.4 * (asl + phw)

######################################################################
# Smog Readability Score
#   http://www.readabilityformulas.com/mcglaughlin-smog-readability-formula.php
# hard is the number of "hard" words, where "hard" means 3 or more syllables
# sent is the number of sentences (careful of sentence fragments)
# SRS = 1.043*sqrt(30 * hard/sent) + 3.1291
#
# Returns a floating point value.
#
def srs(text, i=0, k=None, csyl = countSyllables):
    '''Calculates the SRS of a text.'''
    # Number of words in the text with 3 or more syllables.
    hard = len( [ w for w in extractWords(text, i, k) if csyl(w) >= 3 ] )
    
    # Number of sentences in the text.
    sent = len( extractSentences(text, i, k) )
    
    # Calculates the SRS.
    return 1.043 * sqrt(30 * hard / sent) + 3.1291

######################################################################
# Reads in text from a file and evaluates its readability. Returns
# None. 
def evalText(file='cat.txt', i=0, k=None, csyl=countSyllables):
    '''Read in a text passage and report readability indexes.'''
    text = flushMarks(getText(file))
    print("Evaluating {}:".format(file.upper()))
    print("  {:5.2f} Lix Readability Formula".format(lix(text, i, k)))
    print("  {:5.2f} Gunning's Fog Index".format(fog(text, i, k, csyl)))
    print("  {:5.2f} Smog Readability Score".format(srs(text, i, k, csyl)))
