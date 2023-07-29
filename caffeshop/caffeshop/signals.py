import os
gi

def delete_image_file(sender, instance, **kwargs):
    old_image = sender.objects.filter(pk=instance.pk)
    if old_image:
        old_image = old_image.get(pk=instance.pk).image
    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
