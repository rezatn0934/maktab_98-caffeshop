import os


def delete_image_file(sender, **kwargs):
    img = kwargs['instance']
    if os.path.exists(img.image.path):
        os.remove(img.image.path)


def change_image(sender, instance, **kwargs):
    old_image = sender.objects.filter(pk=instance.pk)
    new_image = instance.image

    if old_image:
        old_image = old_image.get(pk=instance.pk).image
    if not old_image == new_image:
        if old_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)


def change_activation(sender, instance, **kwargs):
    qs = sender.objects.all().update(is_active=False)
    instance.is_active = True
