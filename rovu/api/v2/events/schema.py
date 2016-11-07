# -*- coding: utf-8 -*-
"""Event GraphQL schema."""
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from rovu.api.v1.events.models import Event


class EvGQLSchema(SQLAlchemyObjectType):
    class Meta:
        model = Event


class Query(graphene.ObjectType):
    events = graphene.List(EvGQLSchema)

    def resolve_events(self, args, context, info):
        query = EvGQLSchema.get_query(context)  # SQLAlchemy query
        return query.all()


schema = graphene.Schema(query=Query)
