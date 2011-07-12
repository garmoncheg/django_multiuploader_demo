from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="images/")
    
    def __unicode__(self):
        return self.image.name