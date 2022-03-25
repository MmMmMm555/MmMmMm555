from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User



# Create your models here.






class Topic(models.Model):
    name = models.CharField( max_length=200 ) 
    def __str__(self):
        return self.name    
     
     
     
          



class Room(models.Model):
    host = models.ForeignKey(User , on_delete=models.CASCADE , null=True) 
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL , null=True) 
    name = models.CharField( max_length=200 )
    description = models.TextField(null=True , blank=True)
    participants = models.ManyToManyField( User , related_name='participants' , blank=True )
    updated = models.DateTimeField( auto_now=True )
    created = models.DateTimeField(  auto_now_add=True )
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name
    
    
    
    
    
    
    
class Message(models.Model):
    user = models.ForeignKey( User , on_delete=models.CASCADE ) 
    room = models.ForeignKey( Room , on_delete=models.CASCADE)
    body = models.TextField( null=False )
    img = models.ImageField( upload_to = 'images/' , blank=True )
    
    # img = models.ImageField( upload_to = 'images' , blank=True , null=True )  
    updated = models.DateTimeField( auto_now=True )
    created = models.DateTimeField(  auto_now_add=True )
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.body[0:30]
    
    
    
# class Filee(models.Model):
#     user = models.ForeignKey(User , on_delete=models.CASCADE) 
#     room = models.ForeignKey(Room , on_delete=models.CASCADE)
#     file = models.FileField( upload_to='files' , blank=True )
#     img = models.ImageField( upload_to='files' , blank=True )
#     updated = models.DateTimeField( auto_now=True )
#     created = models.DateTimeField(  auto_now_add=True )
    
#     class Meta:
#         ordering = ['-created']
    
    