from django.db.models import IntegerField

# Used for _logical_shard for hidden model
# _logical_shard = sharding_models.ShardingIntegerField(

class ShardingIntegerField(IntegerField):
    
