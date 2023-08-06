
# FIXME: Add caching of clients

def create(session, name):
    return session.client(name)