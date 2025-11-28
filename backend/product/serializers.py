from rest_framework.serializers import ModelSerializer
from . import models

class ProductSerialzier(ModelSerializer):

    class Meta:
        model = models.Product
        