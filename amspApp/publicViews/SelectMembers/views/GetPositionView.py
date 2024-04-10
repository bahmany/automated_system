from rest_framework import views

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.CompaniesManagment.models import Company
from amspApp.MyProfile.models import Profile


class GetPositionViewset(views.APIView):
    def GetCurrentPositionDocumentInstance(self, request):
        if (request.user.is_active == False):
            return None
        currentPosition = PositionsDocument.objects.filter(userID=request.user.id,
                                                           companyID=request.user.current_company.id)

        if currentPosition.count() == 1:
            profileInstance = Profile.objects.get(userID=request.user.id)

            if currentPosition[0].profileName == "" or currentPosition[0].profileName == None:
                currentPosition[0].update(set__profileName=profileInstance.extra["Name"])

            currentPosition.serial = PositionDocumentSerializer(instance=currentPosition[0]).data
            return currentPosition[0]
        currentPosition = PositionsDocument.objects.filter(userID=request.user.id)
        if currentPosition.count() == 0:
            raise Exception("This position has no company")

        request.user.current_company = Company.objects.get(id=currentPosition[0].companyID)
        request.user.save()

        currentPosition.serial = PositionDocumentSerializer(instance=currentPosition[0]).data
        return currentPosition[0]




    def GetPositionUerProfileName(self, posInstance):
        profileName = "کاربر حذف شده است"
        if posInstance.userID and posInstance.chartID:
            profileName = posInstance.profileName + " - " + posInstance.chartName
        return profileName

    def GetNecInfoOfPos(self, posIntance):
        posDoc = PositionDocumentSerializer(instance=posIntance).data
        return {
            "profileName": posDoc["profileName"],
            "chartName": posDoc["chartName"],
            "avatar": posDoc["avatar"]
        }
