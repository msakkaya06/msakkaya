# easymanagement/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from easymanagement.models import Desk


@receiver(post_save, sender=Desk)
def add_to_group(sender, instance, created, **kwargs):
    if created:
        print(f"{instance.name} grubuna ekleniyor...")  # Debugging için
        channel_layer = get_channel_layer()
        group_name = f"business_{instance.business.id}"

        async_to_sync(channel_layer.group_add)(
            group_name,
            "desk_channel"
        )

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "update_desk",
                "desk_id": instance.id,
                "name": instance.name,
                "is_reserve": instance.isReserve,
                "is_active": instance.isActive,
            }
        )
