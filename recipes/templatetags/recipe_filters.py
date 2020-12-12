from django import template

register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def add_tag_color(tag_obj):
    if tag_obj.slug == "breakfast":
        return "orange"
    elif tag_obj.slug == "lunch":
        return "green"
    elif tag_obj.slug == "dinner":
        return "purple"


@register.filter
def get_tags(tag):
    return tag.getlist("tag")


@register.filter
def get_tags_link(request, tag):
    new_request = request.GET.copy()
    if tag.slug in request.GET.getlist("tag"):
        filters = new_request.getlist("tag")
        filters.remove(tag.slug)
        new_request.setlist("tag", filters)
    else:
        new_request.appendlist("tag", tag.slug)
    return new_request.urlencode()
