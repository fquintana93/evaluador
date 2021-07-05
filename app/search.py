from flask import current_app
from flask_login import current_user

def left(s):
    return s[:(len(s)-2)]

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    #empresa = empresa
    search = current_app.elasticsearch.search(
        index= index,
        body={
                 
            'query': {'multi_match': 
                      {'query': left(query), 
                        'fields': ['rut']
                        },
                      },
                                       
            "sort" :{"_id":"desc"} ,
        #     "mappings": {
        # "properties": {
        #     "correlativo": { "type": "integer" }}
        #                 },
        #     "sort" : [ { "correlativo" : {"order" : "desc"}} ] ,

             'from': (page - 1) * per_page, 'size': per_page
                                
        })
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']









