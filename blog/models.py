from django.db import models

STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
)

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tags = models.CharField(max_length=200, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title + ' by ' + str(self.author)