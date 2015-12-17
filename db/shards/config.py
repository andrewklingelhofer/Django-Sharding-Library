class sharded_config(object):
    def __init__(self, config_dict):
        self._shard_groups = {}
        self._db_config = self.process(config_dict)

    @property
    def db_config(self):
        return self._db_config

    @property
    def shard_groups(self):
        return self._shard_groups

    def process(self, config_dict):
        db_config = {}

        for db in config_dict['unsharded']:
            db_config[db] = config_dict['unsharded'][db]

        for shard_group in config_dict['sharded']:
            logical_shards = config_dict['sharded'][shard_group]['logical_shards']
            del config_dict['sharded'][shard_group]['logical_shards']
            physical_shards = []
            dbs = config_dict['sharded'][shard_group]

            for db in dbs:
                db_config[db] = dbs[db]
                physical_shards.append(db)

            self.shard_groups[shard_group] = {
                'logical_shards': logical_shards,
                'physical_shards': physical_shards
            }

        return db_config
