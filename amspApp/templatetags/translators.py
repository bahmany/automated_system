from asq.initiators import query
from django import template
from django.core.cache import cache
from django.template.defaultfilters import stringfilter
from django.utils.timezone import get_current_timezone
from translate import Translator

from amspApp.Administrator.Languages.serializers.LanguagesSerializer import LanguagesSerializer
from amspApp.models import Languages

register = template.Library()


@register.filter
@stringfilter
def translate(text):
    langs = cache.get("languages")
    if langs == None:
        translateItem = list(Languages.objects.all().values("fa", "en", "ar", "kr").order_by("id"))
        for t in translateItem:
            t["search"] = t["en"].replace(' ', '').lower()
        cache.set("languages", translateItem, 900)
        langs = cache.get("languages")

    translateItem = list(query(langs).where(lambda en: en["search"] == text.replace(' ', '').lower()))
    if len(translateItem) == 0:  # not found
        data = {
            "en": text,
            "fa": text,
        }
        newdt = LanguagesSerializer(data=data)
        vl = newdt.is_valid()
        if vl == False:
            drf = Languages.objects.filter(en=text).order_by("id")
            if (drf.count() != 0):
                if get_current_timezone().zone == "Asia/Tehran":
                    return drf[0].fa
                else:
                    return drf[0].en
            return text
        newdt.save()
        translateItem.append({
            "en": text,
            "fa": text,
            "search": text.replace(' ', '').lower()
        })
        cache.set("languages", translateItem, 900)
        return text

    if get_current_timezone().zone == "Asia/Tehran":
        return translateItem[0]["fa"]
    return translateItem[0]["en"]


def translateToEn(text):
    translator = Translator(from_lang="fa", to_lang="en")
    translation = translator.translate(text)
    return translation
