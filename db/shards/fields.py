from django.db.models.fields import Field
from django.db.models import ForeignKey


class RootKey(Field):

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


class ParentKey(ForeignKey):

    """Defines a child of a sharded tree hierarchy"""

    def __init__(self, **kwargs):
        """

        :parent: Must have a RootKey field defined

        """
        self._parent = kwargs['to']

        ForeignKey.__init__(self, **kwargs)

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
