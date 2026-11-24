from app.errors import NotFound


def get_doc(store, doc_id):
    doc = store.get(doc_id)
    if doc is None:
        raise NotFound(doc_id)
    return doc
