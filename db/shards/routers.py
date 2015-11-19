"""
    Routes sharded data to correct database based on sharding id
"""

class ShardingRouter(objects):
    
    def db_for_read(self, model, **hints):
        """ 
            returns the database based on which database the info
            should go to
        """

    def db_for_write(self, model, **hints):
        """ 
            Calls db_for_read so it knows which database to write
            the info to
        """

    def allow_relation(self, obj1, obj2, **hints):
        """ Not sure if we need this """
            
    def allow_migrate(self, db, app_label, model=None, **hints):
        """ Not sure if we need this """

