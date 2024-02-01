from django.db import connection, models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, phone_number=None, is_active=True, is_customer=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password) # change user password
        user_obj.phone_number = phone_number
        user_obj.customer = is_customer
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_customeruser(self, email, full_name=None, password=None, phone_number=None):
        user = self.create_user(
                email,
                full_name=full_name,
                password=password,
                is_customer=True,
                phone_number=phone_number
        )
        return user

    def create_superuser(self, email, full_name=None, password=None, phone_number=None):
        user = self.create_user(
                email,
                full_name=full_name,
                password=password,
                is_customer=False,
                is_admin=True,
                phone_number=phone_number
        )
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True, db_index=True)
    full_name   = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    phone_number = models.PositiveBigIntegerField(unique=True, db_index=True)
    is_active   = models.BooleanField(default=True) # can login 
    customer    = models.BooleanField(default=False) # customer user non superuser
    admin       = models.BooleanField(default=False) # superuser 
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] #['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return f"{self.email}:::{self.phone_number}"

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_customer(self):
        return self.customer

    @property
    def is_admin(self):
        return self.admin

class BusinessCategory(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        return self.name
    
    def __str__(self):
        return self.display_name

class Business(models.Model):
    category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, db_index=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        return self.name
    
    def __str__(self):
        return self.display_name

class Item(models.Model):
    name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        return self.name
    
    def __str__(self):
        return self.display_name

class BusinessItem(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, db_index=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, db_index=True, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class UserBusinessVolume(models.Model):
    unique_id = models.CharField(max_length=255, primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_phone_number = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    business_category = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    item_name = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField(db_index=True)

    @classmethod
    def refresh_view(cl):
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW user_business_volume")

    class Meta:
        managed = False
        db_table='user_business_volume'