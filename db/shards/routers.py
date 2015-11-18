

class ShardedRouter(objects):
    
    def db_for_read(self, model, **hints):
        

    def db_for_write(self, model, **hints):

    def allow_relation(self, obj1, obj2, **hints):
        """ Not sure if we need this """
            
    def allow_migrate(self, db, app_label, model=None, **hints):
        """ Not sure if we need this """

