from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=100,blank=True,default="")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Id:{self.id}:{self.title} by {self.author} ${self.price}'

