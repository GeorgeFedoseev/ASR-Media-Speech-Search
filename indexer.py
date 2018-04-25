# =* coding: utf-8 *=

import os
import const

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.index import open_dir

from whoosh.qparser import QueryParser

import Stemmer

from whoosh.analysis import StemmingAnalyzer, LanguageAnalyzer
from whoosh.lang.snowball import RussianStemmer




from utils import db_util


import sys
reload(sys)

sys.setdefaultencoding("utf-8")

def index_all():    
    db_util.init_db()

    stemmer = Stemmer.Stemmer('russian')
    whoosh_ru_stemmer = RussianStemmer()

    analyzer = LanguageAnalyzer('russian')

    schema = Schema(transcription_id=ID(stored=True),  transcript=TEXT(stored=True, analyzer=analyzer))
    if not os.path.exists(const.TRANSCRIBED_WHOOSH_INDEX_DIR_PATH):
        os.makedirs(const.TRANSCRIBED_WHOOSH_INDEX_DIR_PATH)

    # recreate new index
    ix = create_in(const.TRANSCRIBED_WHOOSH_INDEX_DIR_PATH, schema)

    writer = ix.writer()

    for item in db_util.get_all_items():
        writer.add_document(transcription_id=str(item.id).decode('utf-8'),            
            transcript=item.transcription
            )    

    

    writer.commit()


def search(q):
    ix = open_dir(const.TRANSCRIBED_WHOOSH_INDEX_DIR_PATH)

    parser = QueryParser("transcript", ix.schema)
    q = q.decode('utf-8')
    query = parser.parse(q)
    
    with ix.searcher() as searcher:
        results = searcher.search(query)

        for r in results:
            print(r.highlights("transcript"))

#ix = open_dir(const.TRANSCRIBED_WHOOSH_INDEX_DIR_PATH)



if __name__ == "__main__":
    #index_all()

    q = "производная"    
    print ("searching for %s" % (q))
    search(q)





