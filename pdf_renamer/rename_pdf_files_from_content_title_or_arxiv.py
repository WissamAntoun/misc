#%%
import os
import sys
import re
import glob
import pdftitle
from tqdm import tqdm
import arxiv
import random
#%%
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.

    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'

    https://github.com/django/django/blob/master/django/utils/text.py
    Copyright (c) Django Software Foundation and individual contributors.
    All rights reserved.
    """
    return re.sub(r'(?u)[^-\w.]', '', s)

#%%
all_files_names = glob.glob("C:\\Users\\WISSAM-PC\\Downloads\\Documents\\*.pdf")
#%%
# research_files = []
# for f in tqdm(all_files_names):
#     try:
#         research_files.append((f,pdftitle.get_title_from_file(f)))
#     except:
#         research_files.append((f,None))   



# %%
research_files = []
for f in tqdm(all_files_names):
    if "__OLDNAME__" in f or '__XX__' in f:
        continue
    basename = os.path.basename(f)
    dirname = os.path.dirname(f)

    if len(re.findall(r'\b\d{4}\.\d{5}',basename)) > 0 :
        article_id = basename.strip('.pdf')
        entry = arxiv.query(id_list=[article_id])
        if len(entry) > 0:
            title = entry[0]['title'].replace(":","")
            title = re.sub(r'\s'," ",title)
            title = get_valid_filename(title)
            new_basename = title + '__OLDNAME__' + basename
            new_path = os.path.join(dirname, new_basename)
    
    else:
        try:
            title = pdftitle.get_title_from_file(f)
            if len(title) < 3:
                continue
            title = re.sub(r'[\\/:"*?<>|]+'," ",title)
            title = re.sub(r'\s'," ",title)
            title = get_valid_filename(title)
            new_basename = title + '__OLDNAME__' + basename
            new_path = os.path.join(dirname, new_basename)
        except:
            title = None
            os.rename(f,f[:-4]+'__XX__'+'.pdf')
            continue

    try:
        print(new_path)
        os.rename(f, new_path)
    except FileExistsError:
        basename = os.path.basename(new_path)
        dirname = os.path.dirname(new_path)
        os.rename(f,os.path.join(dirname, new_basename[:-4]+str(random.randint(0,999))+'.pdf'))
    except:
        os.rename(f,f[:-4]+'__XX__'+'.pdf')
        print('skipping')


# %%
