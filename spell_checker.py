import streamlit as st
import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))
letters    = 'abcdefghijklmnopqrstuvwxyz'
def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    if known(inserts1(word)):
        return known(inserts1(word))
    elif known(transposes(word)):
        return known(transposes(word))
    elif known(replaces(word)):
        return known(replaces(word))
    elif known(inserts2(word)):
        return known(inserts2(word))
    else:
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts    = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))



### UTILITY FUNCTIONS
def inserts1(word):
    splits = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    return [L + c + R               for L, R in splits for c in letters]

def inserts2(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    return [i2 for i1 in inserts1(word) for i2 in inserts1(i1)]

def transposes(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    return [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]

def replaces(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    return [L + c + R[1:]           for L, R in splits if R for c in letters]

random_word = ["","apple","lamon","speling","hapy","language","greay","plot","amuse","rider","weak","likie",
                "slop","urgency","volcanp","central","cafe",
                "groam","release","fead","limit","prescriptoon"]

st.write("# Spellchecker Demo")
add_side_checkbox = st.sidebar.checkbox(
    "Show original word"
)
select_word = st.selectbox('Choose a word or....',random_word)
own_words = st.text_input('type your own!!',select_word)
if add_side_checkbox:
    st.write(f"Original word: {own_words}")
if own_words:
    correct_own_words = correction(own_words)
    if own_words == correct_own_words:
        st.success(f'{own_words} is the correct spelling')
    else:
        st.error(f'Correction: {correct_own_words}')
