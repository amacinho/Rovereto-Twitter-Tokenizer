# -*- coding: utf-8 -*-

"""
Tokenizer for Twitter-based text. Written by AmaÃ§ Herdagdelen 2011.The code is licensed under the Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0.html

For emoticon and URL recognition, this code uses parts of TweetMotif (https://github.com/brendano/tweetmotif). TweetMotif is also licensed under the Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0.html
"""
# TODO: Deal with intensified emoticons like :))))?
# TODO: Deal with Asian-style emoticons or westernized-Asian like (-_-) or (;_;) or (^_^)
# Refer to http://en.wikipedia.org/wiki/Emoticon

# TODO: Implement an option for locale settings:
# Number, date, etc.

import re
import sys
from aux import url
from aux import emoticon

def unicode_compile(regexp):
    return re.compile(ur'%s' % regexp.decode("utf-8"), re.U|re.I)

DEBUG = False
if len(sys.argv) > 1:
    DEBUG = True

clitics = r''

""" For future reference
English, French and Italian clitics:
English post-clitics: 's, 're, 've, 'd, 'm, 'em, 'll, n't
French pre-clitics: d', D', c', C', j', J', l', L', m', M', n', N', s', S', t', T', qu', Qu', jusqu', Jusqu', lorsqu', Lorsqu'
French post-clitics: -t-elles?, -t-ils?, -t-on, -ce, -elles?, -ils?, -je, -la, -les?, -leur, -lui, -mÃªmes?, -m', -moi, -nous, -on, -toi, -tu, t', -vous, -en, -y, -ci, -lÃ 
Italian pre-clitics: dall', Dall', dell', Dell', nell', Nell', all', All', d', D', l', L', sull', Sull', quest', Quest', un', Un', senz', Senz', tutt', Tutt'
"""

html_entity = r'&(amp|lt|gt|quot);'
hashtag = r'#[\w0-9_-]+'
username = r'@[\w0-9_-]+'
punctuation = r'[.\$"\\\'#+!%^*()[\]\-={}|\:;<>,?/`]'
abbrevations = r'([\w]\.){2,}(?![^ ])'
emails = r'[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
first_layer_tokens = [url,
                      abbrevations,
                      emails,
                    ]
second_layer_tokens = [html_entity,
                       hashtag,                       
                       username,
                       emoticon,                                              
                      ]
#if clitics:
#    second_layer_tokens.append(clitics)

third_layer_tokens = [punctuation,                      
                     ]

first_layer_recognizers = [unicode_compile(r'(%s)' % reg) for reg in first_layer_tokens]
second_layer_recognizers = [unicode_compile(r'(%s)' % reg) for reg in second_layer_tokens]
third_layer_recognizers = [unicode_compile(r'(%s)' % reg) for reg in third_layer_tokens]

first_layer_validators = [unicode_compile(r'^%s$' % reg) for reg in first_layer_tokens]
second_layer_validators = [unicode_compile(r'^%s$' % reg) for reg in second_layer_tokens]
third_layer_validators = [unicode_compile(r'^%s$' % reg) for reg in third_layer_tokens]

def is_token(el):    
    for reg in first_layer_validators:
        if reg.match(el):
            return True
    for reg in second_layer_validators:
        if reg.match(el):
            return True
    if re.match('^[\w]+$', el, re.U):
        return True    
    return False
    
def debug_log(msg):
    if DEBUG:
        sys.stderr.write("DEBUG\t%s\n" % msg.strip().encode("utf8"))

def preprocess(content, recognizers):
    debug_log("Before preprocess: %s" % content)    
    for reg in recognizers:
        content = reg.sub(r' \1 ', content)
        debug_log("preprocess: %s" % content)
    return content

def tokenize(content):
    tokens = list()
    content = re.sub(ur'[\n\r\t]', ' ', content)
    content = content.decode("utf8")    
    tokens = list()
    for pre_token in content.split():        
        if is_token(pre_token):
            tokens.append(pre_token)
            debug_log("Accepted in first layer: %s" % pre_token)
            continue
        else:
            elements = preprocess(pre_token, first_layer_recognizers).split()            
            for element in elements:
                if is_token(element):                    
                    tokens.append(element)
                    debug_log("Accepted in second layer: %s" % element)
                    continue
                else:
                    for x in preprocess(element, second_layer_recognizers).split():
                        if is_token(x):
                            debug_log("Accepted in third layer: %s" % x)
                            tokens.append(x)
                        else:
                            for y in preprocess(x, third_layer_recognizers).split():
                                debug_log("Accepted in fourth layer: %s" % y)
                                tokens.append(y)
                                debug_log(y)
    return [x.encode("utf8") for x in tokens]

if __name__ == "__main__":
    txt = "RT @justinbieber: and that's for those that dont know...they've great records like this. #GREATMUSIC: http://www.youtube.com/watch?v=cF"
    print " ".join(tokenize(txt))
