from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address_user')
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    alley = models.CharField(max_length=200)
    plaque = models.CharField(max_length=200)
    postalـcode = models.CharField(max_length=200)
    extra_comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.state} / {self.city} / {self.street}"


def resume_upload_to(instance, filename):
    return f"account/resume/{instance.user.username}/{filename}"


class PdfResume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="pdfResume_user")
    # one to one file: if user want to upload new resume the last resume will gone.
    file = models.FileField(blank=True, null=True, upload_to=resume_upload_to)

    def __str__(self) -> str:
        return self.user.username 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    address = models.ManyToManyField(Address, related_name='profile_address')
    uploaded_resume = models.OneToOneField(PdfResume, on_delete=models.CASCADE, related_name="profile_pdfResume", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_profile_images(self):
        domain_url = settings.DOMAIN_URL
        images_url = []
        for profile_image in self.profileImage_profile.all():
            images_url.append( {'image':domain_url+profile_image.image.url})
        return list(images_url)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def image_upload_to(instance, filename):
    return f"account/profile/{instance.user.username}/{filename}"

class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profileImage_profile'  )
    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)

    def __str__(self) -> str:
        return self.profile.user.username
    
