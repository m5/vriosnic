"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from vriosnic.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine

id = lambda: sa.Column("id",sa.types.Integer, primary_key=True)
name = lambda: sa.Column("name", sa.types.String)
foreign = lambda n,t: sa.Column(n, sa.types.Integer, sa.ForeignKey(t+'.id'))
text = lambda n: sa.Column(n, sa.types.String)

users_table = sa.Table("Users", meta.metadata,
    id(),
    name(),
    text("password"),
    text("email"),
    text("first_name"),
    text("last_name"),
    )

orgs_table = sa.Table("Orgs", meta.metadata,
    id(),
    name(),
    foreign("permission_id", "Permissions"),
    )

roles_table = sa.Table("Roles", meta.metadata,
    id(),
    name(),
    )

events_table = sa.Table("Events", meta.metadata,
    id(),
    name(),
    foreign("org_id","Orgs"),
    )

recurrences_table = sa.Table("Recurrences", meta.metadata,
    id(),
    name(),
    text("rrule"),
    foreign("parent_id", "Events"),
    )

permissions_table = sa.Table("Permissions", meta.metadata,
    id(),
    name(),
    foreign("role_id","Roles"),
    )

class User(object): pass
class Org(object): pass
class Event(object): pass
class Permission(object): pass
class Recurrence(object): pass

orm.mapper(User, users_table)

orm.mapper(Org, orgs_table,
           properties={
               'permissions': sa.orm.relation(
                   Permission,
                   primaryjoin = orgs_table.c.permission_id == permissions_table.c.id,
                   )
                }
           )

orm.mapper(Event, events_table, properties={
    'org': sa.orm.relation(
        Org,
        primaryjoin = events_table.c.org_id == orgs_table.c.id,
        backref='events'
        ),
    })

orm.mapper(Permission, permissions_table)
orm.mapper(Recurrence, recurrences_table)

## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
