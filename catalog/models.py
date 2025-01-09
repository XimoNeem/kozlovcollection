from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    photo = models.ImageField(upload_to='authors/')

    def __str__(self):
        return self.name
    
    

class Work(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='works/')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='works')

    def __str__(self):
        return self.title