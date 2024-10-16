from django.db import models
from Admin.models import tbl_place
# Create your models here.

class tbl_designer(models.Model):
    designer_name = models.CharField(max_length=30)
    designer_email = models.CharField(max_length=30)
    designer_contact = models.CharField(max_length=30)
    designer_password = models.CharField(max_length=30)
    designer_address = models.CharField(max_length=50)
    designer_photo = models.FileField(upload_to="Assets/Designer/Photo")
    designer_proof = models.FileField(upload_to="Assets/Designer/Proof")
    designer_doj = models.DateField(auto_now_add=True)
    designer_status = models.IntegerField(default=0)
    place = models.ForeignKey(tbl_place, on_delete=models.CASCADE)

class tbl_company(models.Model):
    company_name = models.CharField(max_length=30)
    company_email = models.CharField(max_length=30)
    company_contact = models.CharField(max_length=30)
    company_password = models.CharField(max_length=30) 
    company_address = models.CharField(max_length=50)
    company_logo = models.FileField(upload_to="Assets/Company/Logo")
    company_proof = models.FileField(upload_to="Assets/Company/proof")
    company_doj = models.DateField(auto_now_add=True)
    company_status = models.IntegerField(default=0)
    place = models.ForeignKey(tbl_place, on_delete=models.CASCADE)
