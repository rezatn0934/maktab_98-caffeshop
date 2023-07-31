import os


def delete_image_file(sender, **kwargs):
    img = kwargs['instance']
    if os.path.exists(img.image.path):
        os.remove(img.image.path)
