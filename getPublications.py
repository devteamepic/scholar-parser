import scholarly
import pandas as pd
from tqdm import tqdm
import time
def get_text(url):
    # print (url)
    # print (url == )    
    try:
        r = requests.get(url)
    except:
        return None
    f = io.BytesIO(r.content)
    document = f
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    content = ''
    try:
        for page in PDFPage.get_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    content = content + element.get_text().replace('\n', " ")
    except:
        return None
    return content

search = scholarly.search_pubs_query('Engineering')
author = []
title = []
abstract = []
date = []
url = []
eprint = []
date = []
texts = []

for i in tqdm(range(1000)):
    publication = next(search)
    # time.sleep(5)
    # publication.fill()    
    # print(publication.bib.get('year'))
    date.append(publication.bib.get('year'))
    author.append(publication.bib.get('author'))
    title.append(publication.bib.get('title'))
    abstract.append(publication.bib.get('abstract'))
    url.append(publication.bib.get('url'))
    eprint.append(publication.bib.get('eprint'))
                    
df = pd.DataFrame(
{
    'author': author,
    'date' : date,
    'title' : title,
    'abstract':abstract,
    'url':url,
    'eprint': eprint
})
# df = df[df['eprint'].notna()]
df = df.dropna()
df.to_csv('result.csv', index = False)