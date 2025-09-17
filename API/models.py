from django.db import models

class Settings(models.Model):
    hour_price = models.CharField(max_length=7)

    class Meta:
        verbose_name_plural = "Settings"

    def __str__(self):
        return "Settings object"

class JobCard(models.Model):
    job_id = models.CharField(max_length=7)
    customer_id = models.CharField(max_length=7)
    hour_price = models.CharField(max_length=7)
    description = models.TextField()
    completed = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "Job card"

    def __str__(self):
        return self.job_id
    

class CustomerTable(models.Model):
    customer_id = models.CharField(max_length=7)
    name = models.CharField(max_length=30)
    car = models.CharField(max_length=30)
    license_plate = models.CharField(max_length=10)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Customer table"

    def __str__(self):
        return self.customer_id
    

class PartsList(models.Model):
    job_id = models.CharField(max_length=7)
    part_id = models.CharField(max_length=7)
    part_name = models.CharField(max_length=30)
    price = models.CharField(max_length=10)
    url = models.TextField()

    class Meta:
        verbose_name_plural = "Parts list"

    def __str__(self):
        return f'{self.job_id}_{self.part_id}'
    

class CheckList(models.Model):
    job_id = models.CharField(max_length=7)
    check_id = models.CharField(max_length=7)
    check_item = models.CharField(max_length=30)
    done = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "Check list"

    def __str__(self):
        return f'{self.job_id}_{self.check_id}'
    

class TimeTable(models.Model):
    job_id = models.CharField(max_length=7)
    time_id = models.CharField(max_length=5)
    calculated_bool = models.CharField(max_length=2)
    time_registry = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = "Time table"

    def __str__(self):
        return f'{self.job_id}_{self.time_id}'