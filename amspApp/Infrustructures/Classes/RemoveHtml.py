from django.utils.html import MLStripper


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()