from datetime import datetime

from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, sh_to_mil
from amspApp.MyProfile.models import Profile
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class ModelViewMongoPosAndComp(viewsets.ModelViewSet):
    convertDateFields = None

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
            if self.convertDateFields:
                for c in self.convertDateFields:
                    request.data[c] = datetime.strptime(sh_to_mil(request.data[c]), "%Y/%m/%d")
                    # request.data["projectStartDate"] = datetime.strptime(sh_to_mil(request.data['projectStartDate']), "%Y/%m/%d")

        return super(ModelViewMongoPosAndComp, self).initial(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        result = super(ModelViewMongoPosAndComp, self).list(request, *args, **kwargs)
        for d in result.data["results"]:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id,
            )
            if positionDoc.count() != 0:
                positionDoc = positionDoc[0]
                profileInstance = Profile.objects.get(userID=positionDoc.userID)
                d["positionName"] = positionDoc.profileName
                d["positionSemat"] = positionDoc.chartName
                d["avatar"] = profileInstance.extra["profileAvatar"]["url"]
            else:
                d["positionName"] = "حذف شده"
                d["positionSemat"] = "حذف شده"
                d["avatar"] = "/static/images/avatar_empty.jpg"
            d["isEditable"] = (d["positionID"] == positionDoc.positionID)

            if self.convertDateFields:
                for cf in self.convertDateFields:
                    if d.get(cf, None):
                        d[cf] = mil_to_sh(d[cf])

        return result

# def handlePosAndCompInInit(request):
#     if request.method != "GET" and request.method != "DELETE":
#         posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
#         request.data["positionID"] = posiIns.positionID
#         request.data["companyID"] = posiIns.companyID
#         return request
