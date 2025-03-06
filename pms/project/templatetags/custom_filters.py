from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return []
    return dictionary.get(key, [])
@register.filter
def lookup(dictionary, key):
    if isinstance(dictionary, dict):  # Ensure it's a dictionary
        return dictionary.get(key, 0)  # Return 0 if key is missing
    return 0 
