from django.db import models

# Create your models here.

class signup(models.Model):
    name=models.CharField(max_length=30,blank=True,null=True)
    email=models.EmailField(unique=True,blank=True,null=True)
    otp=models.CharField(max_length=6,default=0,blank=True,null=True)
    password=models.CharField(max_length=30, null=True)

    def __str__(self) -> str:
        return self.name

class categories(models.Model):
    name=models.CharField(max_length=30,blank=True,null=True)

    def __str__(self) -> str:
        return self.name

class products(models.Model):
    categories_id = models.ForeignKey(categories,on_delete=models.CASCADE,blank=True,null=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    img = models.ImageField(upload_to="media", blank=True, null=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name





