from django.db import models


class Account(models.Model):
    email = models.TextField()
    full_name = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'test_account'

    @property
    def is_authenticated(self):
        return True


class AppUser(models.Model):
    name = models.TextField()
    email = models.TextField()
    age = models.IntegerField()
    country = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'test_users'
