import bgdb

# Overarching session class for bdgdb
class BGDBSession:
    def __init__(self, db_url, env_mode=False):

        # Establish a client connection
        self.client = bgdb.Client(db_url)

        # Login
        self.client.login(use_env=env_mode)

        # Setup search session
        self.search = bgdb.Search(self.client)
