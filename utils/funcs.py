from sorl.thumbnail import get_thumbnail, delete

def get_sized_image(img, size_tuple=None):

    if size_tuple is not None and isinstance(size_tuple, tuple):
        return get_thumbnail(str(img),"%sx%s"%(size_tuple))
        
    else:
        return img