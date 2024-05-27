from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class UserType(models.Model):
    usertype = models.CharField(max_length=50)

    def __str__(self):
        return self.usertype
    
    class Meta:
      db_table  = 'UserType'

class User(AbstractUser):
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    usertype = models.ForeignKey(UserType, on_delete=models.CASCADE)
    
    class Meta:
      db_table  = 'UserMaster'
    
    # class Meta:
    #     abstract = True

    # def save(self, *args, **kwargs):
    #     if not self.usertype_id:
    #         default_usertype, created = UserType.objects.get_or_create(usertype='Admin')
    #         self.usertype = default_usertype
    #     super().save(*args, **kwargs)



# class Nation(models.Model):
#     nation = models.CharField(max_length=50)

#     def __str__(self):
#         return self.nation

# class State(models.Model):
#     nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
#     state = models.CharField(max_length=50)

#     def __str__(self):
#         return self.state

# class City(models.Model):
#     state = models.ForeignKey(State, on_delete=models.CASCADE)
#     city = models.CharField(max_length=50)
#     pincode = models.CharField(max_length=10)

#     def __str__(self):
#         return self.city