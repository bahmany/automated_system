from datetime import datetime
from rest_framework import serializers
from rest_framework.fields import Field, CharField
from rest_framework.serializers import ModelSerializer
from rest_framework_mongoengine.serializers import DocumentSerializer
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionSerializer, \
    PositionDocumentSerializer
from amspApp.CompaniesManagment.models import Company
from amspApp.MyProfile.models import Profile
from amspApp._Share.DynamicFieldModelSerializer import DynamicFieldsModelSerializer
from amspApp.amspUser.models import MyUser
from amspApp.CompaniesManagment.Secretariat.models import Secretariat


__author__ = 'mohammad'
# class MembersSerializer(DynamicFieldsModelSerializer):
class MembersSerializer(ModelSerializer):
    userName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Position
        # fields = ("id","post_date","userName")
        depth = 0

    def get_userName(self, obj):
        if obj.user :
            profileName = Profile.objects.get(userID=obj.user_id)
            result = {
                "name": profileName.extra["Name"],
                "avatar": profileName.extra["profileAvatar"]["url"],
                "job": obj.chart.title
            }
        else :
            result = {
                "name": "",
                "avatar": "",
                "job": obj.chart.title
            }
        return result


    # here is very important
    def create_in_mongo(self, data, positionInstance):


        # here i clear all person with current position ID
        # and this position become out of person


        if "user" in data:

            # this is means that when we want to clear a position chart id
            # and emptize an active position
            if data["user"] == None:
                posInstance = self.instance
                pos = PositionsDocument.objects.get(
                    positionID = posInstance.id
                )
                finalChanges = {
                    "chartID": posInstance.chart_id,
                    "companyID": posInstance.company_id,
                    "userID": pos.userID,
                    "dateof": datetime.now()
                }

                ll = pos.last
                if ll == None:
                    ll = [finalChanges]
                else:
                    ll.append(finalChanges)
                pos.last = ll
                pos.userID = None
                pos.profileID = None
                pos.avatar = None
                pos.profileName = None
                pos.save()
                return pos
        profileInstance = None
        if positionInstance.user_id:
            profileInstance = Profile.objects.get(userID=positionInstance.user_id)
        final = {}
        if self.partial:

            profileName = None
            userID = None
            if profileInstance:
                if "job" in profileInstance.extra:
                    if "Shenasnameh" in profileInstance.extra["job"]:
                        if "Name" in profileInstance.extra["job"]["Shenasnameh"]:
                            if "Family" in profileInstance.extra["job"]["Shenasnameh"]:
                                profileName = profileInstance.extra["job"]["Shenasnameh"]["Name"] + " " + profileInstance.extra["job"]["Shenasnameh"]["Family"]
                if profileName == None:
                    if "Name" in profileInstance.extra:
                        profileName = profileInstance.extra["Name"]

                if not "user" in data:
                    userID = positionInstance.user_id
                if userID == None:
                    userID = data["user"] if type(data["user"]) == int else data["user"].id


            final = {
                'chartID': positionInstance.chart.id,
                'positionID': positionInstance.id,
                'profileID': profileInstance.id.__str__() if profileName else None,
                'userID': userID if userID else None,
                'companyID': positionInstance.company.id,
                'chartName': positionInstance.chart.title,
                'profileName': profileName  if profileName else None,
                'avatar': profileInstance.extra["profileAvatar"]["url"] if profileName else None,
                'companyName': positionInstance.company.name,
                'post_date': data["post_date"] if "post_date" in data else datetime.now()
            }
            posDoc = PositionsDocument.objects.filter(
                positionID = self.instance.id
            ).order_by("-id")
            if posDoc.count() != 0 :
                posDocSerial = MembersDocumentSerializer(instance=posDoc[0], data=final, partial=True)
                posDocSerial.is_valid(raise_exception=True)
                posDocSerial.update(instance=posDoc[0], validated_data=posDocSerial.validated_data)
                return
            else :
                posDocSerial = MembersDocumentSerializer(data=final)
                posDocSerial.is_valid(raise_exception=True)
                posDocSerial.save()
                return
        else:
            profileName = ""
            if "job" in profileInstance.extra:
                if "Shenasnameh" in profileInstance.extra["job"]:
                    if "Name" in profileInstance.extra["job"]["Shenasnameh"]:
                        if "Family" in profileInstance.extra["job"]["Shenasnameh"]:
                            profileName = profileInstance.extra["job"]["Shenasnameh"]["Name"] + " " + profileInstance.extra["job"]["Shenasnameh"]["Family"]

            final = {
                'chartID': data["chart"].id,
                'profileID': profileInstance.id.__str__(),
                'userID': data["user"].id if data["user"] != None else None,
                'companyID': data["company"].id,
                'chartName': data["chart"].title,
                'profileName': profileName,
                'avatar': profileInstance.extra["profileAvatar"]["url"],
                'companyName': data["company"].name,
                'positionID':positionInstance.id
            }


        poss = PositionsDocument.objects.filter(
            companyID=data["company"].id,
            userID=data["user"] if type(data["user"]) == int else data["user"].id
        )
        if poss.count() != 0:
            raise serializers.ValidationError({"status": "Bad request", "message": {
                "Created Before": ["This user has an chart position before, first you must faceout it"]}})

        newPost = PositionsDocument.objects.create(**final)
        return


    def create(self, validated_data):
        if type(validated_data['chart']) == int:
            validated_data["chart"] = Chart.objects.get(id=validated_data["chart"])
        if type(validated_data['company']) == int:
            validated_data["company"] = Company.objects.get(id=validated_data["company"])
        if type(validated_data['user']) == int:
            validated_data["user"] = MyUser.objects.get(id=validated_data["user"])

        # if validated_data['chart'].set_position.all().count() != 0:
        # raise serializers.ValidationError({"status": "Bad request", "message": {
        # "Created Before": ["This user has an chart position before, first you must faceout it"]}})


        if Position.objects.filter(user=validated_data["user"], company=validated_data["company"]).count() != 0:
            # raise serializers.ValidationError({"status": "Bad request", "message": {
            #     "Created Before": ["This user has an chart position before, first you must faceout it,"]}})
            posss = Position.objects.filter(user=validated_data["user"], company=validated_data["company"])
            for eP in posss:
                updating = {
                    "user":None,
                }
                serP = PositionSerializer(instance=eP, data=updating, partial=None)
                serP.is_valid(raise_exception=True)
                serP.update(instance=serP, validated_data=updating)


        positionInstace = super(MembersSerializer, self).create(validated_data)
        self.create_in_mongo(validated_data, positionInstace)
        return positionInstace

    def update(self, instance, validated_data):
        updatedPosition = super(MembersSerializer, self).update(instance, validated_data)
        self.create_in_mongo(validated_data, updatedPosition)
        return updatedPosition


class MembersDocumentSerializer(DocumentSerializer):
    userID = serializers.IntegerField(required=False, allow_null=True)
    profileID = serializers.CharField(required=False, allow_null=True)
    profileName = serializers.CharField(required=False, allow_null=True)
    avatar = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = PositionsDocument
        fields = (
            'avatar',
            'chartID',
            'chartName',
            'companyName',
            'id',
            'positionID',
            'profileID',
            'profileName',
            'userID',
        )


    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

class MembersDocumentSerializerForPerm(DocumentSerializer):
    userID = serializers.IntegerField(required=False, allow_null=True)
    profileID = serializers.CharField(required=False, allow_null=True)
    profileName = serializers.CharField(required=False, allow_null=True)
    avatar = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = PositionsDocument


    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

