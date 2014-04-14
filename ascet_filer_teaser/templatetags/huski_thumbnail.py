import os
import Image
from django.template import Library

register = Library()

def thumbnail(file, size='104x104', noimage=''):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    try:
        filehead, filetail = os.path.split(file.path)
    except:
        return ''
    basename, format = os.path.splitext(filetail)
    #quick fix for format
    if format.lower() =='.gif':
        return (filehead + '/' + filetail).replace(MEDIA_ROOT, MEDIA_URL)
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    #fail on missing large file (bad import)
    try:
        if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
    except:
        return ''

    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        try:
            image = Image.open(filename)
        except:
            return ''
        image.thumbnail([x, y], Image.ANTIALIAS)
        image.convert('RGB')
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            try:
                image.save(miniature_filename, image.format, quality=90)
            except:
                return noimage

    return miniature_url

register.filter(thumbnail)
from django.conf import settings
MEDIA_ROOT, MEDIA_URL = settings.MEDIA_ROOT, settings.MEDIA_URL

def thumbnail_crop(file, size='104x104', noimage=''):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    try:
        filehead, filetail = os.path.split(file.path)
    except:
        return '' # '/media/img/noimage.jpg'

    basename, format = os.path.splitext(filetail)
    #quick fix for format
    if format.lower() =='.gif':
        return (filehead + '/' + filetail).replace(MEDIA_ROOT, MEDIA_URL)

    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    try:
        if os.path.exists(miniature_filename) and os.path.exists(filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
    except:
        return ''
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        try:
            image = Image.open(filename)
        except:
            return '(minfail %s) ' % filename #noimage

        src_width, src_height = image.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = x, y
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = int(float(src_width - crop_width) / 2)
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = int(float(src_height - crop_height) / 3)
        try:
            image = image.crop((x_offset, y_offset, x_offset+int(crop_width), y_offset+int(crop_height)))
            image = image.resize((dst_width, dst_height), Image.ANTIALIAS)
            image.convert('RGB')
        except:
            pass
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            try:
                image.save(miniature_filename, image.format, quality=90)
            except:
                return '' #'/media/img/noimage.jpg'

    return miniature_url

register.filter(thumbnail_crop)

