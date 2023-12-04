from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Customer(Model):
    # Primary key field is created automatically
    # id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=32)
    phone = fields.CharField(max_length=32)
    assistant_id = fields.CharField(max_length=32)
    thread_id = fields.CharField(max_length=32)
    info = fields.TextField()

    def __str__(self):
        return f'name:{self.name}|phone:{self.phone}|' \
               f'assistant_id:{self.assistant_id}|thread_id:{self.assistant_id}|' \
               f'created:{self.created}'

    class Meta:
        table = 'customer'
        unique_together = (("name", "phone"),)


Customer_Pydantic = pydantic_model_creator(Customer, name='Customer')


class ChatMessage(Model):
    # Primary key field is created automatically
    # id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    chat_id = fields.CharField(max_length=32)
    name = fields.CharField(max_length=32)
    content = fields.TextField()

    def __str__(self):
        return f'chat_id:{self.chat_id}|name:{self.name}|' \
               f'content:{self.content}|created:{self.created}'

    class Meta:
        table = 'chat_message'
        indexes = (('name',), ('chat_id',))


ChatMessage_Pydantic = pydantic_model_creator(ChatMessage, name='ChatMessage')


class ProductCatalog(Model):
    # Primary key field is created automatically
    # id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=64, unique=True)
    type = fields.CharField(max_length=64)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    desc = fields.TextField()

    def __str__(self):
        return f'name:{self.name}|type:{self.type}|' \
               f'price:{self.price}'

    class Meta:
        table = 'product_catalog'


ProductCatalog_Pydantic = pydantic_model_creator(ProductCatalog, name='ProductCatalog')
