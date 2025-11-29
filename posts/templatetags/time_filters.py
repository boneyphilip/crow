from django import template

register = template.Library()


@register.filter
def clean_time(value):
    """Simplify naturaltime output by removing long fragments."""
    if not value:
        return ""

    text = str(value)

    # If naturaltime gives "2 weeks, 4 days ago"
    if "," in text:
        text = text.split(",")[0].strip()

    # Guarantee clean spacing
    text = text.replace("  ", " ").strip()

    return text
