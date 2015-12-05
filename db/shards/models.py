# Model for user in Django App

# Imports (Not sure what's needed yet)

from django.db.models import Model
from django.db.models.fields.related import ForeignKey

class ShardedForeignKey(ForeignKey):
    def __init__(self, ... , **kwargs):

class LogicalShardOptions():
    def __init__(self, physical_shard, shard_num):
        self.physical_shard = physical_shard
        self.shard_num = shard_num
        self.name = None # Name of particular shard
        self.model = None # Type of model this shard contains

    @property
    def is_logical_shard(self):
        # This is a logical shard
        return True

    @property
    def is_physical_shard(self):
        # This is not a physical shard
        return False
    
    @property
    def physical_shard_key(self):
        return self.physical_shard. 

    def get_database(self):
        # Return database of logical shard
        physical_shard = self.physical_shard


class PhysicalShardOptions():
    def __init__(self, options, logical_shards=[]):
        self.options = options # Options of the physical shard
        self.logical_shards = logical_shards # Logical Shard info for cluster
        self.model = None # Type of model this physical shard may use?
        self.name = None # Name of cluster

    @property
    def is_logical_shard(self):
        return False

    @property
    def is_physical_shard(self):
        return True

