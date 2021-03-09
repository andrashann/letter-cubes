from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

import os
import codecs

from sympy.utilities.iterables import multiset_permutations
import jinja2

app = FastAPI(
    title="Words in letter blocks",
    description='''If you have a set of cubes with letters on them and are 
    trying to figure out which words you can make using them, this is the 
    API you need.
    
[https://github.com/andrashann/words-in-letter-blocks](https://github.com/andrashann/words-in-letter-blocks)
''',
    version="0.0.1",
    docs_url="/", redoc_url=None,
)


@app.get("/c/{cubes}", response_class=HTMLResponse)
def get_caches(cubes: str, dic: str = "en/en_US.dic", json: bool = False):
    '''Based on a comma separate list of the set of letters on each cube,
    e.g. 'abcdef,ghijkl,mnopqr' and a 'dic', it returns a list of words
    that are valid in that language and you could come up with using these
    cubes. 

    The dic parameter should be the path to a dictionary in the LibreOffice
    GitHub repository, e.g. "en/en_US.dic" for 
    https://raw.githubusercontent.com/LibreOffice/dictionaries/master/en/en_US.dic.

    If json=True, it returns a JSON list.'''

    cubes = cubes.split(',')

    if not os.path.exists('dic'):
        os.makedirs('dic')

    # If we do not have the dictionary file yet, download it
    filename = dic.split('/')[-1]
    if not os.path.exists(filename):
        import urllib.request
        urllib.request.urlretrieve(f'https://raw.githubusercontent.com/LibreOffice/dictionaries/master/{dic}',
                                   filename)
    else:
        print('Dictonary file already exists.')

    word_list = []

    # The .dic format has extra information about each word at the end,
    # separated by a symbol, so split the line there.
    with codecs.open(filename, encoding='utf-8') as f:
        for word in f.readlines():
            word_list.append(word.split('/')[0].split('\t')[0].strip())

    results = []
    for word in word_list:
        found_match = False

        # don't even look at words that are not the right length
        if len(word) != len(cubes):
            continue

        # letters might appear on multiple cubes, so we should check
        # all possible orders of cubes:
        for cube_list in multiset_permutations(cubes):
            if found_match == True:
                break

            for i, letter in enumerate(word):
                if letter not in cube_list[i]:
                    break
                # if we are at the last letter and everything worked out,
                # the word is a match!
                if i == len(word) - 1:
                    found_match = True
                    results.append(word)

    results = sorted(list(set(results)))

    if json:
        return JSONResponse(content=results)

    template = jinja2.Template('''
    <html><head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>Words in letter blocks</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <meta property="og:title" content="Words in letter blocks" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="http://hann.io/words-in-letter-blocks/og.jpg" />
    <meta property="og:description" content="Find the words you can make out of the letters on letter blocks" />

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
    </head><body>
    <div class="container" style="max-width: 800px;">
      <h1>Words in your blocks</h1>
      <ol>
        {% for e in results %}<li>{{ e }}</li>{% endfor %}
      </ol>
    </div>
    </body></html>''')

    return(template.render(results=results))
