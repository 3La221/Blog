from PIL import Image
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile.pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        # Rotate the image based on EXIF orientation
        if hasattr(img, '_getexif'):
            exif = img._getexif()
            if exif is not None:
                orientation_key = 274  # EXIF tag code for orientation
                if orientation_key in exif:
                    orientation = exif[orientation_key]
                    # Rotate the image
                    if orientation == 1:
                        # Normal image, no rotation needed
                        pass
                    elif orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)

        # Resize the image if necessary
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            
        # Save the image
        img.save(self.image.path)
