# Routes sharded data to correct database based on sharding id
from models import logical_to_physical, shard
from helpers import find_shard_key

class ShardedRouter(object):

    def get_database(self, shard_key):
        return logical_to_physical(shard(shard_key))

    def db_for_read_or_write(self, model, **hints):
        # Returns the database based on which database the info
        # should go to
        db = None
        try:
            instance = hints['instance']
            shard_key = instance.shard_key
            db = self.get_database(shard_key)
        except KeyError:
            print "No instance in hints"
            try:
                db = self.get_database(hints['shard_key'])
            except KeyError:
                print "No shard_key in hints"
        print "Returning", db
        return db
        
    def db_for_read(self, model, **hints):
        return self.db_for_read_or_write(model, **hints)

    def db_for_write(self, model, **hints):
        # Calls db_for_read so it knows which database to write
        # the info to
        return self.db_for_read_or_write(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        # Not sure if we need this
        return True
            
    def allow_migrate(self, db, app_label, model=None, **hints):
        # Not sure if we need this
        return True
