from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from userrequirement.models import UserRequirement
from userrank.models import UserRank

@receiver(post_save, sender=UserRequirement, dispatch_uid="1")
def updateRank(sender, instance,  **kwargs):
    if instance.requirement.is_last:
        if instance.completed:
            try:
                rank = UserRank.objects.get(user=instance.user,rank=instance.requirement.rank)
            except UserRank.DoesNotExist:
                rank = UserRank(user=instance.user,
                                rank=instance.requirement.rank,
                                authorized_by=instance.signed_by)
            
            rank.completed_date=instance.completed_date
            rank.notes=instance.notes
            rank.authorized_by=instance.signed_by
            rank.earned=True
            rank.save()