from .database import local_session

def get_DB ():
    DB = local_session()
    try:
        yield DB
    finally:
        DB.close()
