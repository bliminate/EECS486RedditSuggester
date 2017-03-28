import re
import sys
import glob
import operator
from wordstem import PorterStemmer
## Elaine Apaza - etapaza

##Contraction dictionary taken from stack overflow
#http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
contractions = { 
	"ain't": "am not",
	"aren't": "are not",
	"can't": "cannot",
	"can't've": "cannot have",
	"'cause": "because",
	"could've": "could have",
	"couldn't": "could not",
	"couldn't've": "could not have",
	"didn't": "did not",
	"doesn't": "does not",
	"don't": "do not",
	"hadn't": "had not",
	"hadn't've": "had not have",
	"hasn't": "has not",
	"haven't": "have not",
	"he'd": "he would",
	"he'd've": "he would have",
	"he'll": "he will",
	"he'll've": "he will have",
	"he's": "he is",
	"how'd": "how did",
	"how'd'y": "how do you",
	"how'll": "how will",
	"how's": "how is",
	"I'd": "I would",
	"I'd've": "I would have",
	"I'll": "I will",
	"I'll've": "I will have",
	"I'm": "I am",
	"I've": "I have",
	"isn't": "is not",
	"it'd": "it would",
	"it'd've": "it would have",
	"it'll": "it will",
	"it'll've": "it will have",
	"it's": "it is",
	"let's": "let us",
	"ma'am": "madam",
	"mayn't": "may not",
	"might've": "might have",
	"mightn't": "might not",
	"mightn't've": "might not have",
	"must've": "must have",
	"mustn't": "must not",
	"mustn't've": "must not have",
	"needn't": "need not",
	"needn't've": "need not have",
	"o'clock": "of the clock",
	"oughtn't": "ought not",
	"oughtn't've": "ought not have",
	"shan't": "shall not",
	"sha'n't": "shall not",
	"shan't've": "shall not have",
	"she'd": "she would",
	"she'd've": "she would have",
	"she'll": "she will",
	"she'll've": "she will have",
	"she's": "she is",
	"should've": "should have",
	"shouldn't": "should not",
	"shouldn't've": "should not have",
	"so've": "so have",
	"so's": "so as",
	"that'd": "that had",
	"that'd've": "that would have",
	"that's": "that is",
	"there'd": "there had",
	"there'd've": "there would have",
	"there's": "there is",
	"they'd": "they had",
	"they'd've": "they would have",
	"they'll": "they will",
	"they'll've": "they will have",
	"they're": "they are",
	"they've": "they have",
	"to've": "to have",
	"wasn't": "was not",
	"we'd": "we had",
	"we'd've": "we would have",
	"we'll": "we will",
	"we'll've": "we will have",
	"we're": "we are",
	"we've": "we have",
	"weren't": "were not",
	"what'll": "what will",
	"what'll've": "what will have",
	"what're": "what are",
	"what's": "what is",
	"what've": "what have",
	"when's": "when is",
	"when've": "when have",
	"where'd": "where did",
	"where's": "where is",
	"where've": "where have",
	"who'll": "who will",
	"who'll've": "who will have",
	"who's": "who is",
	"who've": "who have",
	"why's": "why is",
	"why've": "why have",
	"will've": "will have",
	"won't": "will not",
	"won't've": "will not have",
	"would've": "would have",
	"wouldn't": "would not",
	"wouldn't've": "would not have",
	"y'all": "you all",
	"y'all'd": "you all would",
	"y'all'd've": "you all would have",
	"y'all're": "you all are",
	"y'all've": "you all have",
	"you'd": "you had",
	"you'd've": "you would have",
	"you'll": "you will",
	"you'll've": "you will have",
	"you're": "you are",
	"you've": "you have"
}


#dates = re.compile("2017.1.11", "1/11/2017", "Jan. 11th, 2017", "12/12/2012", "January 8, 2017")

stopwords = open('stopwords', "r")
lines = stopwords.readlines()
stopList = []

for line in lines:
	stopList.append(line.rstrip())

def removeSGML(line):
	if '<' and '>' in line:
		return ''
	else:
		return line


###############Remove the SGML Tags from the Text ################



#################### Tokenize the text ################################

def isInt(num):
	try: 
		int(num)
		return True
	except ValueError:
		return False

def tokenizeText(line):
	words = line.split()
	tokens = []

	for word in words:

		# deal with .
		if '.' in word:
			if len(word) == 1:
				donothing=1
			#elif word.len() > 1 and 
			elif (len(word)-1) == word.index('.') and isInt(word[len(word)-2]):
				word = word[:-1]
				tokens.append(word)
			else:
				#deals with dates that are separated by periods here
				tokens.append(word)

		
		##deal with '
		elif '\'' in word:
			##If the word is a contraction, split it up and add the words separately 
			if word in contractions:
				newvalue = contractions[word]
				temp = newvalue.split()

				for wd in temp:
					tokens.append(wd)

			else:
				newvalue = word.split('\'')
				ct = 0	
				for wd in newvalue:
					if ct == 0:
						tokens.append(wd)
					else:
						tokens.append('\''+wd)
					ct += 1;


		##deal with -  
		elif '-' in word:
			if len(word) == 1:
				donothing = 0
			else:
				tokens.append(word)

		##deal with , 
		elif ',' in word:
			if isInt(word[word.index(',')-1]):
				tokens.append(word)
			else:
				temp = word.split(',')
				for wd in temp:
					tokens.append(wd)

		else:
			tokens.append(word)
	return tokens


def removeStopwords(tokenList):
	newTokenList = []
	for token in tokenList:
		if token not in stopList:
			newTokenList.append(token)

	return newTokenList



def stemWords(tokenList):
	#print("cool")
	stemmer = PorterStemmer()
	stems = []
	for token in tokenList:
		stems.append(stemmer.stem(token, 0, len(token)-1))

	return stems


