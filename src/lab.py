import attr


@attr.s
class Lab(object):
    name = attr.ib(validator=attr.validators.instance_of(str), default='')
    faculties = attr.ib(validator=attr.validators.instance_of(list), default=attr.Factory(list))
    professors = attr.ib(validator=attr.validators.instance_of(list), default=attr.Factory(list))
    description = attr.ib(validator=attr.validators.instance_of(str), default='')
    url = attr.ib(validator=attr.validators.instance_of(str), default='')