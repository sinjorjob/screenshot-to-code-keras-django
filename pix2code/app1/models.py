from django.db import models


class Document(models.Model):
    
    document = models.ImageField(verbose_name="File Upload", upload_to='png/')
 

