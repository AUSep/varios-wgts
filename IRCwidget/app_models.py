from peewee import SqliteDatabase, Model, CharField, TextField, DateTimeField, BlobField
from datetime import datetime

db = SqliteDatabase('varios_widgets/IRCwidget/test.db')
now = datetime.now()

class ImpResponses(Model):
    name = CharField(default='default_name', column_name = 'Nombre')
    description  = TextField(default='default_description', column_name = 'Descripción')
    DateTime = DateTimeField(default = now, column_name = 'Fecha de captura')
    response_file = BlobField(column_name='Archivo IR')

    class Meta():
        database = db

db.connect()
db.create_tables([ImpResponses])
