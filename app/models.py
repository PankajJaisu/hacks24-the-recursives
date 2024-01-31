from django.db import models

# Create your models here.



# class Rating(models.Model):
#     mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200,null=True,blank=True)
#     rating = models.IntegerField(null=True,blank=True)
#     description = models.CharField(max_length=240,null=True,blank=True)



class AIDesign(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    image_url = models.CharField(max_length=300, null=True,blank=True)
   