# Model for user in Django App

# Imports (Not sure what's needed yet)

from django.db.models import Model
from django.db.models.fields.related import ForeignKey

class ShardedForeignKey(ForeignKey):
    # This should be pretty much similar to Django's ForeignKey, except 
    # It will also work similarly to ManyToManyField, 
    # because our ForeignKey isn't a ForeignKey, it's
    # a sharding id and connector to all other aspects 
    # of the databases. In order to find a partition,
    # you must know it's id, therefore everything 
    # in some way can be connected to another. This needs to 
    # be clearly defined in the definitions here
    def __init__(self, to, on_delete=None, related_name=None, related_query_name=None, limit_choices+to=None, parent_link=False, to_field=None, db_constraint=True , **kwargs):
        try:
            to._meta.model_name # May need to change this because it may not account for our model
        except AttributeError:
            assert isinstance(to, six.string_types), (
                "%s(%r) is invalid. First parameter to ForeignKey must be 
                either a model, a model name, or the string %r" % (
                    self.__class__.__name__, to, RECURSIVE_RELATIONSHIP_CONSTANT,
                )
            )
        else:
            to_field = to_field or (to._meta.pk and to._meta.pk.name) # Not completely sure what this does yet
        
        kwargs['rel'] = self.rel_class(
            self, to, to_field,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            on_delete=on_delete, # Not sure if we need this
        )

        super(ForeignKey, self).__init__(
            to, on_delete, from_fields=['self'], to_fields=[to_field], **kwargs
        )

        self.db_index = True

        # defs for ForeignKey, we don't need a lot of them for now because they aren't relevant to sharding
        # Either that, or we don't need to implement them again

        def contribute_to_class(self, cls, name): 
            # This is normally contained within ManyToManyField, but it's relevant here.
            # This is because we want to support multiple relations to the self, because of partitioning.
            # Except now, as opposed to ManyToManyField, we want the super to be ForeignKey
            super(ForeignKey, self).contribute_to_class(cls, name, **kwargs)
            
            setattr(cls, self.name, ShardedDescriptor(self))

        def contribute_to_related_class(self, cls, related):
            # What goes here?
            return



def create_logical_shard(physical_shard, shard_number):
    # Creates and sets up new logical shard. This is called when making a new partition for sharding.

class LogicalShardOptions(object):
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


class PhysicalShardOptions(object):
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

# This is used in conjunction with the ShardedForeignKey as an attribute of the ForeignKey
class ShardingDescriptor(ModelBase):
    

# Our model a user uses for sharding data, based off our ShardingDescriptor
class ShardingModel(Model):
    __metaclass__ = ShardingDescriptor

    class Meta:
        abstract = True
