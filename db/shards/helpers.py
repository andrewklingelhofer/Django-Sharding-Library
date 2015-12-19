def find_shard_key(instance):
    key = None
    for field in instance._meta.concrete_fields:
        field_name = str(field).split('.')[-1]
        if getattr(field, 'sharding_root', False):
            key = getattr(instance, field_name)
            break
        elif getattr(field, 'child_key', False):
            rel_instance = getattr(instance, field_name)
            key = getattr(rel_instance, '_shard_key', None)
            if key is None:
                key = find_shard_key(rel_instance)
            break
    else:
        raise Exception("No sharding root")
    return key
