from django.db import models
from datetime import date

class PresentationData(models.Model):
    entry_id = models.CharField(max_length=20, unique=True, editable=False,blank=True)
    date = models.DateField(default=date.today,blank=True)
    toname = models.CharField(max_length=200)
    phno = models.CharField(max_length=10)
    aadharno = models.CharField(max_length=12)
    ap1 = models.CharField(max_length=100)
    ap2 = models.CharField(max_length=100, blank=True)
    aptdas = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.entry_id:
            super().save(*args, **kwargs)  # Save so id exists
            self.entry_id = f"IVFAP{self.id}"
            # Save again with entry_id
            super().save(update_fields=["entry_id"])
        else:
            super().save(*args, **kwargs)
