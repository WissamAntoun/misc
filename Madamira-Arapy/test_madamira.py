#%%
from arapy.madamira import Madamira

#%%
text = "ما هي صفات السبعين ألفا الذين يدخلون الجنة بغير حساب"

with Madamira() as m:
    out = m.process([text])

# %%
for doc in out.docs():
    for sent in doc.sentences():
        for word in sent.words():
            print(word.get_orig_word(),": ", word.pos(),"--",word.get_attribute('gen'),"--",word.get_attribute('per'))


# %%
