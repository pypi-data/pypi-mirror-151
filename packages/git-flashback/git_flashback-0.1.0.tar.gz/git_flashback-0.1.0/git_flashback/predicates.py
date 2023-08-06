def issubclass_by_name(cls, other):
    return cls.__qualname__ == other.__qualname__ or issubclass(other, cls)


def isinstance_by_name(inst, cls):
    return inst.__class__.__qualname__ == cls.__qualname__ or isinstance(inst, cls)


def issubclass_by_qualname(cls, other):
    return cls.__qualname__ == other.__qualname__ or issubclass(other, cls)


def isinstance_by_qualname(inst, cls):
    return inst.__class__.__qualname__ == cls.__qualname__ or isinstance(inst, cls)
