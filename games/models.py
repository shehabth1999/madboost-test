from django.db import models

# Create your models here.
class Game(models.Model):
  name = models.CharField(max_length=100)
  link = models.CharField(max_length=100)

  logo_image = models.ImageField(upload_to='games/logos/', blank=True, null=True)
  banner_image = models.ImageField(upload_to='games/banners/', blank=True, null=True)
  name_image = models.ImageField(upload_to='games/names/', blank=True, null=True)

  def __str__(self):
    return self.name
  
  def get_logo_image_url(self):
    return f"/media/{self.logo_image}"
  
  def get_banner_image_url(self):
    return f"/media/{self.banner_image}"
  
  def get_name_image_url(self):
    return f"/media/{self.name_image}"