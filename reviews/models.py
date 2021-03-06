from django.db import models
from profiles.models import UserProfile
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='userreview')
    subject = models.CharField(max_length=20, null=False, blank=False)
    review = models.TextField(null=False, blank=False)
    rating = models.DecimalField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ], default=0, max_digits=4, decimal_places=1, null=False, blank=False)
    product_id = models.IntegerField(null=False, blank=True)
    order_number = models.CharField(max_length=32, null=False, blank=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.product_id)
