from itertools import cycle
from django.db import models

from manager import ShardedManager
from helpers import find_shard_key


class RootKey(models.Field):

    """Defines the root of a sharded tree hierarchy"""

    def __init__(self, sharding_function='modulo', *args, **kwargs):
        """

        :sharding_function: How this model will be sharded

        """
        self._sharding_function = sharding_function

        return super(RootKey, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(RootKey, self).deconstruct()
        del kwargs['sharding_function']

        return name, path, args, kwargs

    @property
    def sharding_function(self):
        return self._sharding_function


class ParentKey(models.ForeignKey):

    """Defines a child of a sharded tree hierarchy"""

    def __init__(self, **kwargs):
        """

        :parent: Must have a RootKey field defined

        """
        self._parent = kwargs['to']

        models.ForeignKey.__init__(self, **kwargs)

        # Check if the related model is defined as a RootKey
        sharding_function = getattr(self.rel, 'sharding_function', None)
        if sharding_function is None:
            # TODO: Create specialized exceptions
            raise Exception("Parent must be a RootKey")

    def deconstruct(self):
        return super(RootKey, self).deconstruct()

    @property
    def parent(self):
        return self._parent


class ShardedModel(models.Model):
    # Abstract base class

    objects = ShardedManager()
    shards = []
    mapping = []
    # mock values
    logical = 16
    physical = ['db1', 'db2']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        shard_key = find_shard_key(self)
        if shard_key:
            setattr(self, '_shard', shard_key)
        else:
            raise Exception("Shard Key was none")
        self.__class__.shards.append(self._shard)
        super(ShardedModel, self).save(force_insert=force_insert, force_update=force_update,
                                       using=using, update_fields=update_fields)

    @classmethod
    def shard(cls, shard_key):
        return shard_key % ShardedModel.logical

    @classmethod
    def logical_to_physical(cls, logical):
        if len(cls.mapping) == 0:
            cycler = cycle(cls.physical)
            while len(cls.mapping) < cls.logical:
                cls.mapping.append(next(cycler))
        return cls.mapping[logical]

    class Meta:
        abstract = True
