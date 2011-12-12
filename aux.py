# encoding: utf-8

# Regular expressions and auxilary functions used in this script are taken from O'Connor et al.'s Tweetmotif
# see: https://github.com/brendano/tweetmotif

import re

def regex_or(*items):
  r = '|'.join(items)
  r = '(' + r + ')'
  return r

def pos_lookahead(r):
  return '(?=' + r + ')'

def neg_lookahead(r):
  return '(?!' + r + ')'

def optional(r):
  return '(%s)?' % r

# Build URL
PunctChars = r'[\'“".?!,:;]'
html_entity = '&(amp|lt|gt|quot);'
UrlStart1 = regex_or('https?://', r'www\.')
CommonTLDs = regex_or('com','co\\.uk','org','net','info','ca')
UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + CommonTLDs + pos_lookahead(r'[/ \W\b]')
UrlBody = r'[^ \t\r\n<>]*?'  
UrlExtraCrapBeforeEnd = '%s+?' % regex_or(PunctChars, html_entity)
UrlEnd = regex_or( r'\.\.+', r'[<>]', r'\s', '$')

url = (r'\b' + 
    regex_or(UrlStart1, UrlStart2) + 
    UrlBody + 
    pos_lookahead( optional(UrlExtraCrapBeforeEnd) + UrlEnd))

# Build emoticon
NormalEyes = r'[:=]'
Wink = r'[;]'
NoseArea = r'(|o|O|-)'  
HappyMouths = r'[D\)\]]'
SadMouths = r'[\(\[]'
Tongue = r'[pP]'
OtherMouths = r'[doO/\\]' 

emoticon = (
    "("+NormalEyes+"|"+Wink+")" +
    NoseArea + 
    "("+Tongue+"|"+OtherMouths+"|"+SadMouths+"|"+HappyMouths+")"
)
