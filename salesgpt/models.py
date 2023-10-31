from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class ChatMessage(Model):
    # Primary key field is created automatically
    # id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    session_id = fields.CharField(max_length=32)
    role = fields.CharField(max_length=32)
    content = fields.TextField()

    def __str__(self):
        return f'session_id:{self.session_id}|role:{self.role}|' \
               f'content:{self.content}|created:{self.created}'

    class Meta:
        table = 'chat_message'
        indexes = (('session_id',),)


ChatMessage_Pydantic = pydantic_model_creator(ChatMessage, name='ChatMessage')


class ProductCatalog(Model):
    # Primary key field is created automatically
    # id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=64)
    type = fields.CharField(max_length=64)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    desc = fields.TextField()

    def __str__(self):
        return f'name:{self.name}|type:{self.type}|' \
               f'price:{self.price}'

    class Meta:
        table = 'product_catalog'
        indexes = (('name',),)


ProductCatalog_Pydantic = pydantic_model_creator(ProductCatalog, name='ProductCatalog')
