from itertools import cycle
from django.db import models
from django.conf import settings

from manager import ShardedManager
from helpers import find_shard_key
from decorators import classproperty


class ShardableModel(models.Model):
    # Abstract base class

    objects = ShardedManager()

    _shards = []
    _mapping = []

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        shard_key = find_shard_key(self)
        if shard_key is not None:
            setattr(self, '_shard_key', shard_key)
        else:
            raise Exception("Shard Key was none")
        self.__class__._shards.append(self._shard_key)
        super(ShardableModel, self).save(force_insert=force_insert, force_update=force_update,
                                         using=using, update_fields=update_fields)

    @classproperty
    @classmethod
    def logical(cls):
        if not getattr(cls, '_logical', None):
            cls._logical = settings.SHARDING.shard_groups[cls.shard_group]['logical_shards']
        return cls._logical

    @classproperty
    @classmethod
    def physical(cls):
        if not getattr(cls, '_physical', None):
            cls._physical = settings.SHARDING.shard_groups[cls.shard_group]['physical_shards']
        return cls._physical

    @classmethod
    def shard(cls, shard_key):
        return shard_key % cls.logical

    @classmethod
    def logical_to_physical(cls, logical):
        mapping = cls._mapping
        if len(cls._mapping) == 0:
            cycler = cycle(cls.physical)
            while len(mapping) < cls.logical:
                mapping.append(next(cycler))
        return mapping[logical]

    class Meta:
        abstract = True
