from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from wildRift.models import WildRiftRank
import secrets
from games.models import Game

class UserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email Field Must Be Set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class BaseUser(AbstractUser):
    country = CountryField(blank=True,null=True)
    is_booster = models.BooleanField(default= False)
    is_customer = models.BooleanField(default= False)
    is_admin = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to='accounts/images/', null=True)

    # customer_rooms = models.ManyToManyField('Room', related_name='customers', blank=True)

    def get_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return None
    
    def save(self, *args, **kwargs):
        if self.is_booster:
            super().save(*args, **kwargs)
        else:
            self.can_choose_me = False
            super().save(*args, **kwargs)
    
# @receiver(post_save, sender=BaseUser)
# def create_wallet(sender, instance, created, **kwargs):
#     if created and instance.is_booster:
#         Wallet.objects.create(user=instance)

@receiver(post_save, sender=BaseUser)
def create_wallet(sender, instance, created, **kwargs):
    print(f"Creating wallet for user {instance.email} - Created: {created}")
    if created:
        wallet, created = Wallet.objects.get_or_create(user=instance)
        print(f"Wallet created: {created}")
    
class Wallet(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE,related_name='wallet')
    money = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Has {self.money}$'

class BoosterPercent(models.Model):
    booster_percent1 = models.IntegerField(default=22)
    booster_percent2 = models.IntegerField(default=24)
    booster_percent3 = models.IntegerField(default=27)
    booster_percent4 = models.IntegerField(default=30)
        
# Base Order
class BaseOrder(models.Model):
    SERVER_CHOICES = [
        (1, 'Europa'),
        (2, 'America'),
        (3, 'Asia'),
        (4, 'Africa'),
        (5, 'Australia'),
        (6, 'North America'),
        (7, 'South America'),
        (8, 'Middle East'),
        (9, 'KRJP'),
    ]
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Droped', 'Droped'),
        ('Extend', 'Extend'),
        ('Done', 'Done'),
        ('Continue', 'Continue'),
    ]
    GAME_TYPE = [
        ('D', 'Division'),
        ('P', 'Placement'),
        ('A', 'Arena')       
    ]
    name = models.CharField(max_length=30, null = True)
    details = models.CharField(max_length=300, default='no details')
    game = models.ForeignKey(Game, null=True, on_delete=models.DO_NOTHING, default=None, related_name='game')
    game_type = models.CharField(max_length=10, choices=GAME_TYPE, null=True)
    price = models.FloatField(default=0, blank=True, null=True)
    actual_price = models.FloatField(default=0, blank=True, null=True)
    money_owed = models.FloatField(default=0, blank=True, null=True)
    invoice = models.CharField(max_length=300)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='New', null=True, blank=True)
    customer = models.ForeignKey(BaseUser, null=True, blank=True, on_delete=models.DO_NOTHING, default=None, related_name='customer_orders', limit_choices_to= {'is_customer': True})
    booster = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.DO_NOTHING, default=None, related_name='booster_division', limit_choices_to={'is_booster': True} ) 
    duo_boosting = models.BooleanField(default=False, blank=True)
    select_booster = models.BooleanField(default=False, blank=True)
    turbo_boost = models.BooleanField(default=False, blank=True)
    streaming = models.BooleanField(default=False, blank=True)
    finish_image = models.ImageField(upload_to='wildRift/images/orders', blank=True, null=True) # TODO not wildRift folder 
    is_done = models.BooleanField(default=False, blank=True)
    is_drop = models.BooleanField(default=False, blank=True)
    is_extended = models.BooleanField(default=False, blank=True)
    customer_gamename = models.CharField(max_length=300, blank=True, null=True)
    customer_password = models.CharField(max_length=300, blank=True, null=True)
    customer_server = models.CharField(max_length=300, blank=True, null=True)   # TODO make it interger filed and relational choise
    data_correct = models.BooleanField(default=False, blank=True)
    message = models.CharField(max_length=300, null=True, blank=True)
    payer_id = models.CharField(blank=True,max_length=50, null=True)
    promo_code = models.FloatField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # this will save relation of order (:
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null= True)
    object_id = models.PositiveIntegerField(null =True)
    related_order = GenericForeignKey('content_type', 'object_id')

    def update_actual_price(self):
        if self.status == 'Continue' or self.status == 'Extend':
            return {'time':-1,'price':self.actual_price,'progress':5}
        current_time = timezone.now()
        
        # TODO make this numbers in json file to stop calling db every time
        percent1 = BoosterPercent.objects.get(pk=1).booster_percent1
        percent2 = BoosterPercent.objects.get(pk=1).booster_percent2
        percent3 = BoosterPercent.objects.get(pk=1).booster_percent3
        percent4 = BoosterPercent.objects.get(pk=1).booster_percent4
        

        # TODO add turbo_boost here to be the max and ignore it from tasks
        if not self.created_at:
            self.actual_price = round(self.price * (percent1 / 100) , 2)
        else:
            time_difference = (current_time - self.created_at).total_seconds()
            if time_difference <= 60:
                self.actual_price = round(self.price * (percent1 / 100), 2)
                data = {'time':int(60-time_difference),'price':self.actual_price,'progress':1}
            elif time_difference <= 180:
                self.actual_price = round(self.price * (percent2 / 100), 2)
                data = {'time':int(180-time_difference),'price':self.actual_price,'progress':2}
            elif time_difference <= 900:
                self.actual_price = round(self.price * (percent3 / 100), 2)
                data = {'time':int(900-time_difference),'price':self.actual_price,'progress':3}
            elif time_difference <= 1800 :
                self.actual_price = round(self.price * (percent4 / 100), 2)
                data = {'time':int(1800-time_difference),'price':self.actual_price,'progress':4}
            else:
                data = {'time':-1,'price':self.actual_price,'progress':5}
        self.save()        
        return data    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_booster_wallet()

    def update_booster_wallet(self):
        if (self.is_done or self.is_drop) and not self.is_extended and self.booster and self.money_owed > 0:
            try:
                booster_wallet = self.booster.wallet
                booster_wallet.money += self.money_owed
                booster_wallet.save()
            except:
                Wallet.objects.create (
                    user=self.booster,
                    money=round(self.money_owed, 3)
                )
 
            if self.is_drop :
                Transaction.objects.create (
                    user=self.booster,
                    amount=round(self.money_owed, 3),
                    order=self,
                    status='Drop',  
                    type='DEPOSIT'
                )

            else :
                Transaction.objects.create (
                    user=self.booster,
                    amount=round(self.money_owed, 3),
                    order=self,
                    status='Done',  
                    type='DEPOSIT'
                )

    def customer_wallet(self):        
        if self.status == 'Drop' or self.status == 'Extend':
            print("Order status is 'Drop' or 'Extend', exiting customer_wallet function")
            return
        
        if self.customer and self.price > 0:
            try: 
                customer_wallet = self.customer.wallet
                customer_wallet.money += self.price
                customer_wallet.save()
                print(f"Customer wallet updated. New balance: {customer_wallet.money}")
            except: 
                Wallet.objects.create (
                    user=self.customer,
                    money=round(self.price, 3)
                )
            
            Transaction.objects.create (
                user=self.customer,
                amount=round(self.price, 3),
                order=self,
                status='New',  
                type='WITHDRAWAL'
            )

    def __str__(self):
        return f'{self.customer} have [{self.game.name.upper()}] order - {self.details}'

class Tip_data(models.Model):
    payer_id            = models.CharField(max_length=50, null=True)
    invoice             = models.TextField(max_length=50)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.payer_id    
    
    @classmethod
    def create_tip(cls, invoice, payer_id) :
        return cls.objects.create(invoice=invoice, payer_id=payer_id)
        

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Drop', 'Drop'),
        ('Extend', 'Extend'),
        ('Done', 'Done'),
        ('Tip', 'Tip')
    ]
    user = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    order = models.ForeignKey(BaseOrder, on_delete=models.DO_NOTHING, related_name='from_order')
    notice = models.TextField(default='_')
    status = models.CharField(max_length=100,choices=STATUS_CHOICES, default='New')
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    tip = models.ForeignKey(Tip_data, related_name='tip', on_delete=models.DO_NOTHING, null=True) 

    def __str__(self):
        return f'{self.user.username} {self.type} {self.amount}$'

    

# ####################### Chat #######################
class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    customer = models.ForeignKey(BaseUser, blank=True, on_delete=models.DO_NOTHING, default=None, related_name='customer_room', limit_choices_to={'is_booster': False})
    booster = models.ForeignKey(BaseUser, null=True, blank=True, on_delete=models.SET_NULL, default=None, related_name='booster_room', limit_choices_to={'is_booster': True} ) 
    order_name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    is_for_admins = models.BooleanField(null=False)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['name', 'customer']]


    def __str__(self):
        return self.slug
    
    @classmethod
    def get_specific_room(cls,customer,order_name):
        slug = f'roomFor-{customer}-{order_name}'
        try :
            room = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            room = None
        return room    
    
    @classmethod
    def get_specific_admins_room(cls,customer,order_name):
        slug=f'roomFor-{customer}-admins-{order_name}'
        try :
            room = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            room = None
        return room    

    @classmethod
    def create_room_with_booster(cls,customer,booster,order_name):
        room = cls.get_specific_room(customer,order_name)
        if not room :
            room = cls.objects.create(
                    name=f'{customer}-{order_name}',
                    slug=f'roomFor-{customer}-{order_name}',
                    customer=customer,
                    booster=booster,
                    order_name=order_name,
                    is_for_admins = False,
                )
        return room  
    
    @classmethod
    def create_room_with_admins(cls,customer,order_name):
        room = cls.get_specific_admins_room(customer,order_name)
        if not room :
            room = cls.objects.create(
                    name=f'{customer}-admins-{order_name}',
                    slug=f'roomFor-{customer}-admins-{order_name}',
                    customer=customer,
                    booster=None,
                    order_name=order_name,
                    is_for_admins = True,
                )
        return room
    
    @classmethod
    def get_all_rooms(cls):
        return cls.objects.all().order_by('-created_on')
    
    
    @classmethod
    def close_the_room(cls, slug):
        room = cls.objects.get(slug=slug) 
        if room:
            room.active = False
            room.save()

    @classmethod
    def reOpen_the_room(cls, slug):
        room = cls.objects.get(slug=slug)
        if room:
            room.active = True
            room.save()
        
    

class Message(models.Model):
    MSG_TYPE = (
        (1, 'normal'),
        (2, 'tip'),
    )
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    msg_type = models.IntegerField(choices=MSG_TYPE, default=1)

    def __str__(self):
        return "Message is :- "+ self.content
    
    @classmethod
    def get_last_msg(cls,room):
        last_message = cls.objects.filter(room=room).order_by('-created_on').first()
        return last_message
    
    @classmethod
    def create_tip_message(cls, user, content, room):
        new_message = cls.objects.create(
            user=user,
            content=content,
            room=room,
            created_on=timezone.now(),
            msg_type= 2
        )
        return new_message
    

class TokenForPay(models.Model):
    user                = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    token               = models.TextField(max_length=40, unique=True)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s token"
    
    @classmethod
    def get_token(cls, token):
        try:
            return cls.objects.get(token=token)
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_token(cls, token):
        try:
            cls.objects.get(token=token).delete()
            return None     
        except cls.DoesNotExist:
            return None    
        

class PromoCode(models.Model):
    code                = models.CharField(max_length=50, unique=True)
    description         = models.CharField(null=True, max_length=50)
    discount_amount     = models.FloatField()
    is_active           = models.BooleanField(default=True)
    expiration_date     = models.DateField()
    max_uses            = models.PositiveIntegerField(default=1)
    times_used          = models.PositiveIntegerField(default=0)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.max_uses == 0:
            permanent = 'Permanent'
            times_left = ''
        else:
            permanent = self.max_uses - self.times_used
            times_left = ' Times Left'
        
        return f'{self.code } | {permanent} {times_left}'

    def can_be_used(self):
        return self.is_active and (self.max_uses == 0 or self.times_used < self.max_uses)

    def use_code(self):
        if self.can_be_used():
            self.times_used += 1
            self.save()
            return True
        return False
    