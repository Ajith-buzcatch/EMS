from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class NationMaster(models.Model):
    nation = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
      db_table  = 'NationMaster'
    
class StateMaster(models.Model):
    nation = models.ForeignKey(NationMaster, on_delete=models.CASCADE, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
      db_table  = 'StateMaster'
    
class CityMaster(models.Model):
    state = models.ForeignKey(StateMaster, on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
      db_table  = 'CityMaster'
    
class DepartmentMaster(models.Model):
    department = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
      db_table  = 'DepartmentMaster'
    
class DesignationMaster(models.Model):
    designation = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
      db_table  = 'DesignationMaster'
      
    
class EmployeeMaster(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='employees', blank=True, null=True)
    employee_code = models.CharField(max_length=50, blank=True, null=True)
    employee_name = models.CharField(max_length=250, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.ForeignKey(CityMaster,on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
      db_table  = 'EmployeeMaster'

class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.ForeignKey(CityMaster, on_delete=models.CASCADE, blank=True, null=True)
    reg_no = models.CharField(max_length=100, blank=True, null=True)
    company_icon = models.ImageField(blank=True, null=True)
    company_logo = models.ImageField(blank=True, null=True)
    
    class Meta:
      db_table  = 'CompanyDetails'
      
class EmployeeJoinMaster(models.Model):
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE, blank=True, null=True)
    join_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
      db_table  = 'EmployeeJoinMaster'

    
class EmployeeDepartment(models.Model):
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(DepartmentMaster,on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
      db_table  = 'EmployeeDepartment'
    
class EmployeeDesignation(models.Model):
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE, blank=True, null=True)
    designation = models.ForeignKey(DesignationMaster,on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
      db_table  = 'EmployeeDesignation'
    
class EmployeeImage(models.Model):
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, blank=True, null=True)
    employee_image = models.ImageField(blank=True,null=True,upload_to='employee_images')
    
    class Meta:
      db_table  = 'EmployeeImage'
      
class AttendanceMaster(models.Model):
    Slno = models.IntegerField(max_length=50, null=True, blank=True)
    employee = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE, blank=True, null=True)
    login_datetime = models.DateTimeField(blank=True, null=True)
    logout_datetime = models.DateTimeField(blank=True, null=True)
    login_ipaddress = models.CharField(max_length=1000, null=True, blank=True)
    logout_ipaddress = models.CharField(max_length=1000, null=True, blank=True)
    
    class Meta:
      db_table  = 'AttendanceMaster'
    
# class TimeBreakMaster(models.Model):
#     tbreak =