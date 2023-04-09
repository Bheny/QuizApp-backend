from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 






class Profile(models.Model):
    image = models.ImageField(upload_to='images/profile/', blank=True)
    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # on create of user account, check if there is an existing profile.
    if created:
        profile = Profile.objects.create(user=instance)
        
 
        
       


# @receiver(post_save, sender=Profile)
# def profile_post_save(sender, instance, **kwargs):
#     print("after",instance.rank)
#     soft = SoftSkill.objects.create(profile=instance)
#     TechnicalSkill = SoftSkill.objects.create(profile=instance)

    
