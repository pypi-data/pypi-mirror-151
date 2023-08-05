from peewee import CharField, IntegerField, Model, DatabaseProxy, \
    DateTimeField, AutoField, ForeignKeyField
from datetime import datetime
from playhouse.shortcuts import ThreadSafeDatabaseMetadata


db = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db
        model_metadata_class = ThreadSafeDatabaseMetadata


class WorkingData(BaseModel):
    name = CharField(unique=True)
    size = IntegerField()
    date = DateTimeField()
    checksum = CharField(null=True)


class Chunk(BaseModel):
    id = AutoField()
    data = ForeignKeyField(WorkingData, backref='chunks',  lazy_load=False,
                           on_delete='CASCADE')
    start = IntegerField()
    end = IntegerField()
    status = CharField()


class CompletedHistory(BaseModel):
    id = AutoField()
    timestamp = DateTimeField(default=datetime.now)
    name = CharField()
    size = IntegerField()
    checksum = CharField(null=True)
