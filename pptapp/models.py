from django.db import models
from datetime import date

class PresentationData(models.Model):
    entry_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    date = models.DateField(default=date.today().strftime("%d/%m/%Y"), blank=True)
    toname = models.CharField(max_length=200)
    phno = models.CharField(max_length=10)
    aadharno = models.CharField(max_length=12)
    ap1 = models.CharField(max_length=100)
    ap2 = models.CharField(max_length=100, blank=True)
    aptdas = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=255, default='', blank=True)
    ap_district = models.CharField(max_length=100,blank=True)       # Just a string
    ap_constitution = models.CharField(max_length=100,blank=True)   # Just a string
    pincode = models.CharField(max_length=10, blank=True, null=True)
    committee=models.CharField(max_length=30,blank=True)
    def save(self, *args, **kwargs):
        if not self.entry_id:
            super().save(*args, **kwargs)
            self.entry_id = f"IVFAP{self.id}"
            super().save(update_fields=["entry_id"])
        else:
            super().save(*args, **kwargs)
