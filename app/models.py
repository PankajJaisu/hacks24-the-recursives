from django.db import models

# Create your models here.




class AIDesign(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    image_url = models.CharField(max_length=300, null=True,blank=True)
   



class ProjectManager(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    academic_background = models.CharField(max_length=255,null=True,blank=True)
    career_path = models.CharField(max_length=255,null=True,blank=True)
    
  
    year_of_experience = models.IntegerField(null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

 


class Rating(models.Model):
    mentor = models.ForeignKey(ProjectManager, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True)
    description = models.CharField(max_length=240,null=True,blank=True)
