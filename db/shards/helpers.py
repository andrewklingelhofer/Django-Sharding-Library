def find_shard_key(instance):
    key = None
    for field in instance._meta.concrete_fields:
        if getattr(field, 'sharding_root', False):
            field = str(field).split('.')[-1]
            key = getattr(instance, field)
            break
    else:
        raise Exception("No sharding root")
    return key
