from mongoengine import DictField
from rest_framework import serializers
from rest_framework.fields import *
# from rest_framework_mongoengine import serializers
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.MyProfile.models import Profile, HiddenProfiles
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from django.utils.translation import ugettext_lazy as _


class ProfileSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = Profile
        depth = 2

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


    def update(self, instance, validated_data):
        # instance.extra = validated_data['extra']
        if instance.extra["Name"] == "":
            raise serializers.ValidationError(
                {"status": "Bad request", "message": [{"name": _("Name"), "message": _("This field is required")}]})
        result = super(ProfileSerializer, self).update(instance, validated_data)
        self.updateOtherResources(validated_data, instance)
        return result


    """
    This procedure updates everything with new profile avatar and name,
    we have lots of models which store profile completely to increase search speed
    the way i am updating is awfull
    but now i have no time to R&D and choose the best way to bulk update
    """

    def updateOtherResources(self, validated_data, oldInstance):
        # getting all inboxes
        # this source is not good so i disabled that
        # inboxQuery = Inbox.objects.filter(sender__userID = oldInstance.userID)
        # for i in inboxQuery:
        # i.sender["avatar"] = validated_data["extra"]["profileAvatar"]["url"]
        #     i.sender["profileName"] = validated_data['extra']['Name']
        #     i.save()
        posQuery = PositionsDocument.objects.filter(userID=oldInstance.userID)
        for p in posQuery:
            p.avatar = validated_data["extra"]["profileAvatar"]["url"].replace("=", "=thmum100_")
            p.profileName = validated_data['extra']['Name']
            p.save()
            # updating inbox completed in mongo now it is time to update elastic
            # --------------------------------------------------
            # now i have to update elastic
            # first i have to get all inbox indexes


    jobDetails = {
        'Shenasnameh': {},
        'Education': {},
        'Language': {},
        'Doreh': {},
        'Experience': {},
        'Software': {},
        'Job': {},
        'Resume': {}
    }


    def defaultExtra(self, userInstance):
        return {"extra": {
            "profileHeaderBackground": {
                "url": "/static/images/person_profile_default.jpg",
            },
            "profileAvatar": {
                "url": "/static/images/avatar_empty.jpg",
            },
            "job":self.jobDetails,
            "Name": str(_("%s - change it please !" % (userInstance.username,))),
            "Title": str(_("Nothing yet..!")),
            "Phones": [],
            "AboutMe": {
                "title": str(_("A little about me")),
                "detail": """
                                    Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum
                                    soluta nobis est eligendi optio
                                    cumque nihil impedit quo minus id quod maxime placeat facer
                """,
            }
        }
        }

    def create_default_profile(self, userInstance):
        returnProfile = self.defaultExtra(userInstance)
        returnProfile["userID"] = userInstance.pk
        returnProfile["emails"] = [userInstance.email, ]
        returnProfile["friends"] = []
        returnProfile["companyMembers"] = []
        obj = Profile.objects.create(**returnProfile)
        return obj



class HiddenProfilesSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = HiddenProfiles
        depth = 2

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)