# Routes sharded data to correct database based on sharding id
from helpers import find_shard_key


class ShardedRouter(object):

    def get_database(self, model, shard_key):
        return model.logical_to_physical(model.shard(shard_key))

    def db_for_read_or_write(self, model, **hints):
        # Returns the database based on which database the info
        # should go to
        db = None
        try:
            instance = hints['instance']
            # check instance chached shard_key (on saves)
            # before finding it by looping through fields
            shard_key = getattr(instance, '_shard_key', None)
            if shard_key is None:
                shard_key = find_shard_key(instance)
            db = self.get_database(model, shard_key)
            print("instance:", instance)
            print("shard_key:", shard_key)
            print("db:", db)
        except KeyError:
            print("No instance in hints")
            try:
                db = self.get_database(model, hints['shard_key'])
            except KeyError:
                print("No shard_key in hints")
        print("Returning", db)
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
