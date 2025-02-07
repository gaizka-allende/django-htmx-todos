# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
#from django.core.validators import MaxValueValidator, MinValueValidator


class Suggestions(models.Model):
    title = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'suggestions'


class Todos(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(blank=True, null=True, max_length=255)
    #completed = models.IntegerField(default=0, validators=[MaxvalueValidator(1), MinvalueValidator(0)]) 
    completed = models.IntegerField(default=0) 
    created_modified = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'todos'
