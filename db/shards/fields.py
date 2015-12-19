from django.db import models
from django.db.models import AutoField


# Used for _logical_shard for hidden model
# _logical_shard = sharding_models.ShardingIntegerField(

class ShardingAutoField(AutoField):
    def db_type(self, *args, **kwargs):
        if not hasattr(self.model, '_sharding_function'):
            raise ValueError("ShardingAutoField needs to be used with ShardingModel.")

    # Next based on database we use


class BigIntegerField(models.BigIntegerField):
    def __init__(self, sharding_root=False, *args, **kwargs):
        super(BigIntegerField, self).__init__(*args, **kwargs)
        self.sharding_root = sharding_root


class ParentKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        super(ParentKey, self).__init__(to, **kwargs)
        self.child_key = True
