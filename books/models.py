from django.db import models

# Create your models here.
class Books(models.Model):
    title = models.CharField("Title",max_length=255)
    description = models.CharField("Description",max_length=255,null=True,blank=True)
    author = models.CharField("Author",max_length=50,null=True,blank=True)
    cover_image = models.FileField("Cover Image",upload_to='books/')

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        verbose_name_plural = "Books"