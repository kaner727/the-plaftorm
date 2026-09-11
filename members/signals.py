from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course, User 

# Automatically enroll new users in a course. 
@receiver(post_save, sender=User)
def auto_enroll_with_first_course(sender, instance, created, **kwargs):
    if created:
        first_course = Course.objects.first()
        
        if not first_course:
            first_course = Course.objects.create(title='Default', description='First course, course ID 1')
        
        instance.course = first_course 
        instance.save() 

#        if instance.is_superuser: 
#            instance.course = first_course
#            instance.save()

