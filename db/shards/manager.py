from django.db import models

from helpers import find_shard_key


class ShardedManager(models.Manager):

    def __init__(self):
        super(ShardedManager, self).__init__()
        # self.queryset_class = ShardedQuerySet

    def _get_queryset(self, instance):
        hints = self._hints
        if hints:
            hints['shard_key': find_shard_key(instance)]
        else:
            hints = {'shard_key': find_shard_key(instance)}
        return self._queryset_class(model=self.model, hints=hints)

    def all(self, instance):
        return getattr(self._get_queryset(instance), 'all')()

    def filter(self, instance, *args, **kwargs):
        return getattr(self._get_queryset(instance), '')(*args, **kwargs)

    def get(self, instance, *args, **kwargs):
        return getattr(self._get_queryset(instance), 'all')(*args, **kwargs)
