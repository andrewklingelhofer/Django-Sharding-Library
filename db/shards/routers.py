# Routes sharded data to correct database based on sharding id

class ShardingRouter(objects):
    
    def db_for_read(self, model, **hints):
        # Returns the database based on which database the info
        # should go to
        sharding_function = self.getattr(model, '_sharding_function', None)
        if sharding_info:
            # If sharding_info exists, make sure it's a logical shard
            if sharding_info.is_logical_shard:
                # This means it can return the database it's located in
                return sharding_info.get_database()
            else:
                raise ValueError('Not a logical shard, can\'t be queried')
        

    def db_for_write(self, model, **hints):
        # Calls db_for_read so it knows which database to write
        # the info to
        hints['is_write'] = True
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        # Not sure if we need this
            
    def allow_migrate(self, db, app_label, model=None, **hints):
        # Not sure if we need this

