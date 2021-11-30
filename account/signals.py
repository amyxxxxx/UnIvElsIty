from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import CustomUser
from django.core.mail import send_mail


@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):

    if created:
        print("i AM WORKING")
        message = f"""Hello, {instance.first_name}.
Your account has been successfully activated.  

        
Regards,
The Django Team.        
        
        """
        
        send_mail(subject="Your Account Has Been Created", 
                 message=message, 
                 recipient_list=[instance.email], 
                 from_email='admin@reportly.com')