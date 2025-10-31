import uuid
from mongoengine import Document, StringField, UUIDField, DateTimeField, ListField
from datetime import datetime

class Post(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4, binary=False)
    title = StringField(required=True)
    excerpt = StringField(required=True)
    tags = ListField(StringField(), default=list)
    content = StringField(required=True)
    updated_at = DateTimeField(default=datetime.now(datetime.timezone.utc))