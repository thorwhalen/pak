__author__ = 'thorwhalen'


def get_db(db_name='test-database'):
    import pymongo as mg
    connection = mg.MongoClient()
    db = connection[db_name]
    return db




