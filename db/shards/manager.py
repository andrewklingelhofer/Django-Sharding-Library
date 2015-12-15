from django.db import models

from helpers import find_shard_key


class ShardedManager(models.Manager):

    def _get_queryset_with_instance(self, instance):
        hints = self._hints
        if hints:
            hints['shard_key'] = find_shard_key(instance)
        else:
            hints = {'shard_key': find_shard_key(instance)}
        return self._queryset_class(model=self.model, hints=hints)

    def _get_queryset_with_shardkey(self, shard_key):
        hints = self._hints
        if hints:
            hints['shard_key'] = shard_key
        else:
            hints = {'shard_key': shard_key}
        return self._queryset_class(model=self.model, hints=hints)

    def _query_with_shardkey_or_instance(self, func_name, *args, **kwargs):
        instance = kwargs.get('instance', None)
        shard_key = kwargs.get('shard_key', None)
        if instance:
            del kwargs['instance']
            return getattr(self._get_queryset_with_instance(instance), func_name)(*args, **kwargs)
        elif shard_key:
            del kwargs['shard_key']
            return getattr(self._get_queryset_with_shardkey(shard_key), func_name)(*args, **kwargs)
        else:
            raise Exception('You must pass either a shard_key or instance as a keyword')

    def all(self, *args, **kwargs):
        return self._query_with_shardkey_or_instance('all', *args, **kwargs)

    def filter(self, *args, **kwargs):
        return self._query_with_shardkey_or_instance('filter', *args, **kwargs)

    def get(self, *args, **kwargs):
        shard_key = kwargs.get('shard_key', None)
        if shard_key:
            return getattr(self._get_queryset_with_shardkey(shard_key), 'get')(*args, **kwargs)
        else:
            raise Exception('Get must be passed a shard_key as a keyword')
