import hashlib
from django.db.models.signals import pre_save
from django.dispatch import receiver
from models import Unit, UnitRequest

@receiver(pre_save, sender=UnitRequest)
def pre_save_invite(sender, instance, **kwargs):
    # set hash key for invite
    if instance.type == 'invite' and instance.key is None or instance.key == "":
        m = hashlib.sha1()
        key = "%s-%s"%(instance.email, instance.member.email)
        m.update(key)
        key = m.hexdigest()
        instance.key = key
