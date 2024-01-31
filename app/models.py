from django.db import models

# Create your models here.


class DailyProgress(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    image_url = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

 


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
    project_manager = models.ForeignKey(ProjectManager, on_delete=models.CASCADE)

    title = models.CharField(max_length=200,null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True)
    description = models.CharField(max_length=240,null=True,blank=True)

class Vendor(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    academic_background = models.CharField(max_length=255,null=True,blank=True)
    per_day_salary = models.CharField(max_length=255,null=True,blank=True)
    year_of_experience = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)



class Task(models.Model):
  
    task_title = models.CharField(max_length=255,null=True,blank=True)
    task_description = models.CharField(max_length=500,null=True,blank=True)
    deadline = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

