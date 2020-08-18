from django.db import models
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=50)
    name = models.CharField(max_length=150) 
    activation_key = models.CharField(blank=True, null=True, max_length=300, unique=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=70)
    image = models.ImageField(upload_to='upload/', blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    facebook = models.CharField(max_length=50, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    active_status = models.BooleanField(default=False)
    status = models.BooleanField(default=False) 

    class Meta: 
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return "{} - {}".format(self.name, self.user_id)

class Judgecat(models.Model):
    category = models.CharField(max_length=300)
    status = models.BooleanField(default=True)

    class Meta: 
        verbose_name = 'Judgecat'
        verbose_name_plural = 'Judgecats'

    def __str__(self):
        return self.category


class Judge(models.Model): 
    name = models.CharField(max_length=100) 
    category = models.ForeignKey(Judgecat, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='upload/')
    country = CountryField()
    desc = RichTextField()
    website = models.CharField(max_length=300, blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    twitter = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:  
        verbose_name = 'Judge'
        verbose_name_plural = 'Judges'

    def __str__(self):
        return self.name


class Copyright(models.Model): 
    title = models.CharField(max_length=200)
    text = models.TextField()
 
    class Meta: 

        verbose_name = 'Copyright'
        verbose_name_plural = 'Copyrights'

    def __str__(self):
        return self.title


class Contest(models.Model): 
    TAGS = (
        ('Ongoing','Ongoing'), 
        ('Upcoming','Upcoming'),
    )
    ENTRY = (
        ('F','Free'),
        ('P','Premium'),
    )
    contest_name = models.CharField(max_length=250)
    start_date = models.DateTimeField(auto_now_add=False)
    ending_date = models.DateTimeField(auto_now_add=False)
    tags = models.CharField(max_length=100, choices=TAGS)
    judges = models.ManyToManyField(Judge)
    thumbnail = models.ImageField(upload_to='upload/')
    theme = models.TextField()
    first_price = models.IntegerField()
    second_price = models.IntegerField()
    third_price = models.IntegerField()
    eligibility = models.CharField(max_length=400)
    entry_type = models.CharField(max_length=2, choices=ENTRY)
    copyright = models.ForeignKey(Copyright, on_delete=models.CASCADE)
    status = models.BooleanField(default=True) 

    class Meta: 
        verbose_name = 'Contest'
        verbose_name_plural = 'Contests'

    def __str__(self): 
        return self.contest_name


class Contestimg(models.Model): 
    photo_id = models.IntegerField()
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='contest-image/')
    image_title = models.CharField(max_length=340)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    class Meta:  
        verbose_name = 'Contestimg'
        verbose_name_plural = 'Contestimgs'

    def __str__(self): 
        return "{} - {}".format(self.image_title, self.photo_id)


class Gallery(models.Model): 
    title = models.CharField(max_length=50)
    gallery_image = models.ImageField(upload_to='upload/')
    gallery_desc = models.TextField()
    announced_date = models.DateTimeField()
    featured = models.BooleanField(default=False)
    judges = models.ManyToManyField(Judge)
    first_place_photo_id = models.IntegerField() 
    second_place_photo_id = models.IntegerField() 
    third_place_photo_id = models.IntegerField()
    best_entry1_id = models.IntegerField(blank=True, null=True)
    best_entry2_id = models.IntegerField(blank=True, null=True)
    best_entry3_id = models.IntegerField(blank=True, null=True)
    best_entry4_id = models.IntegerField(blank=True, null=True)
    best_entry5_id = models.IntegerField(blank=True, null=True)
    best_entry6_id = models.IntegerField(blank=True, null=True)
    best_entry7_id = models.IntegerField(blank=True, null=True)
    best_entry8_id = models.IntegerField(blank=True, null=True)
    best_entry9_id = models.IntegerField(blank=True, null=True)
    best_entry10_id = models.IntegerField(blank=True, null=True)
    best_entry11_id = models.IntegerField(blank=True, null=True)
    best_entry12_id = models.IntegerField(blank=True, null=True)
    best_entry13_id = models.IntegerField(blank=True, null=True)
    best_entry14_id = models.IntegerField(blank=True, null=True)
    best_entry15_id = models.IntegerField(blank=True, null=True)
    best_entry16_id = models.IntegerField(blank=True, null=True)
    best_entry17_id = models.IntegerField(blank=True, null=True)
    best_entry18_id = models.IntegerField(blank=True, null=True)
    best_entry19_id = models.IntegerField(blank=True, null=True)
    best_entry20_id = models.IntegerField(blank=True, null=True)
    best_entry21_id = models.IntegerField(blank=True, null=True)
    best_entry22_id = models.IntegerField(blank=True, null=True)
    best_entry23_id = models.IntegerField(blank=True, null=True)
    best_entry24_id = models.IntegerField(blank=True, null=True)
    best_entry25_id = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True) 
    class Meta: 
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'

    def __str__(self): 
        return self.title