from django import template


register = template.Library()


@register.filter(name="img")
def standar_image(value):
    if value == "":
        image = 'images/product/empty.jpg'
        return image
    else:
        return value
