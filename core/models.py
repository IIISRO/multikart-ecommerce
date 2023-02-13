from django.db import models

# Create your models here.


class AbstractModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Contact(AbstractModel):
    first_name = models.CharField('Fisrt name', max_length=15)
    last_name = models.CharField('Last name', max_length=15)
    number = models.CharField('Contact number', max_length=15)
    email = models.EmailField('Email')
    message = models.CharField("Message", max_length=200)

    def __str__(self):
        return f'{self.first_name}{self.last_name}==>{(self.message)[:50]}'


class BlockedIp(AbstractModel):
    ip = models.CharField(max_length=20)

    def __str__(self):
        return self.ip

