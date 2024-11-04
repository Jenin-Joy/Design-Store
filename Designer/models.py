from django.db import models
from Guest.models import tbl_designer,tbl_company
# Create your models here.

class tbl_design(models.Model):
    design_caption = models.CharField(max_length=30)
    design_rate = models.CharField(max_length=30)
    design_file = models.FileField(upload_to='Assets/Designer/Designs/')
    design_upload_date = models.DateField(auto_now_add=True)
    design_description = models.CharField(max_length=100)
    design_status = models.IntegerField(default=0)
    designer = models.ForeignKey(tbl_designer, on_delete=models.CASCADE)

class tbl_designcopyright(models.Model):
    design = models.ForeignKey(tbl_design, on_delete=models.CASCADE)
    company = models.ForeignKey(tbl_company, on_delete=models.SET_NULL, null=True)
    copyright_date = models.DateField(auto_now_add=True)
    copyright_status = models.IntegerField(default=0)

class tbl_complaint(models.Model):
    complaint_title = models.CharField(max_length=30)
    complaint_content = models.CharField(max_length=200)
    complaint_reply = models.CharField(max_length=200)
    complaint_status = models.IntegerField(default=0)
    designer = models.ForeignKey(tbl_designer, on_delete=models.CASCADE)