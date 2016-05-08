# Django-Sharding-Library
A work-in-progress sharding library for Django. Currently supports MySQL and PostgreSQL.

# How to use:

- Download/clone this repo
- Place the db/shards folder in your Django folder for applications

# Example

in settings.py:
```
DATABASE_ROUTERS = ['sharding.models.ShardedRouter']

SHARDING = sharded_config(
{
     'unsharded': {
          'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         },
     },
     'sharded': {
         'shard_group_one': {
             'logical_shards': 1024,
             'db1': {
                 'ENGINE': 'django.db.backends.sqlite3',
                 'NAME': os.path.join(BASE_DIR, 'db1.sqlite3'),
             },
             'db2': {
                 'ENGINE': 'django.db.backends.sqlite3',
                 'NAME': os.path.join(BASE_DIR, 'db2.sqlite3'),
             }
         }
     }
 })

 DATABASES = SHARDING.db_config
```

 in models.py:

```
 class Test(ShardableModel):

     shard_group = 'shard_group_one'

     shard_key = BigIntegerField(sharding_root=True)


 class Post(ShardableModel):
     shard_group = 'shard_group_one'
     post_id = ParentKey(Test)
```
