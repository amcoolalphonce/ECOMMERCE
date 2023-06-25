from django.db import models
from django.utils.text import slugify #find out what slugify 
import secrets # for generating API keys


STATUS_CHOICES=(
    ('sub', 'Received'),
    ('sta', 'Started'),
    ('comp', 'Completed')
)


class Order(models.Model):
    amount=1200
    email=models.EmailField("Email" , default="amcoolalphonce@gmail.com")
    first_name=models.CharField("First Name",max_length=20)
    last_name=models.CharField('Last Name' ,max_length=20)
    telephone_number=models.CharField('Telephone Number', max_length=20)
    date_brought=models.DateField('Date of Order')
    phone_model=models.CharField('Phone Model', max_length=20)
    description=models.TextField('Description of repair', blank=True)
    status=models.CharField(max_length=4, choices=STATUS_CHOICES, default='sub')
    class Meta:
        verbose_name='Phone Repair Order'
        verbose_name_plural='Phone Repair Orders'
    def __str___(self) ->str:
        return self.first_name


STATUS_OPTIONS=(
    ('ava', 'Availabe'),
    ('nav', 'Not Availabe'),
    ('rec', 'Received')
)

class Spareparts(models.Model):
    first_name=models.CharField("First Name", max_length=20)
    telephone=models.CharField("Telephone Number", max_length=20)
    phone_model=models.CharField('Phone Model', max_length=20)
    spare=models.CharField("Spare Part", max_length=50)
    email=models.EmailField("Email " , default="amcoolrepairshop@gmail.com")
    status=models.CharField(max_length=4, choices=STATUS_OPTIONS, default='rec')
    class Meta:
        verbose_name='Sparepart'
        verbose_name_plural='Spareparts'
    def __str__(self) -> str:
        return self.first_name

class Payment(models.Model):
    amount=models.PositiveBigIntegerField()
    ref=models.CharField(max_length=200)
    email=models.EmailField()
    verified=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=['date_created', ]
    
    def __str__(self) -> str:
        return f'Payment: {self.amount}'

    def save(self, *args, **kwargs) ->None:
        while not self.ref:  #while it has no reference
            ref=secrets.token_urlsafe(50)
            object_with_similar_ref=Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref=ref
        super().save(*args, **kwargs)
    
    def amount_value(self) ->int:
        return self.amount* 1
