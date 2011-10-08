from django.contrib.admin.widgets import AdminFileWidget
from django.conf import settings
from django.utils.safestring import mark_safe

from utils.funcs import get_sized_image

def thumbnail(image_path):
    t = get_sized_image(image_path, (50, 50))
    return u'<img style="float:left;margin-right:5px;" src="%s" alt="%s">' % (t.url, image_path)

class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        if value:
            file_path = '%s%s' % (settings.MEDIA_URL, value)
            try:
                output.append('<a target="_blank" href="%s">%s</a>' %
                        (file_path, thumbnail(value)))
            except IOError:
                output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' %
                        ('Currently:', file_path, value, 'Change:'))

        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))