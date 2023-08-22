from django.db import models

class Tag(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    # writer = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    hit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    @property
    def update_counter(self):
        self.hit += 1
        self.save()
        return self.hit
