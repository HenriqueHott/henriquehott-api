import uuid
from mongoengine import Document, StringField, UUIDField, DateTimeField, ListField
import datetime

class Post(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4, binary=False)
    title = StringField(required=True)
    excerpt = StringField(required=True)
    tags = ListField(StringField(), default=list)
    content = StringField(required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    
    meta = {
        
        "collection": "posts",
    }
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "excerpt": self.excerpt,
            "tags": self.tags,
            "content": self.content,
            "updated_at": self.updated_at.isoformat(),
        }