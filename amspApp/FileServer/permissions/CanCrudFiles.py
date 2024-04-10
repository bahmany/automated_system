from rest_framework import permissions

from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.views.CompaniesManagmentView import CompaniesManagmentViewSet
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class CanCruidFiles(permissions.BasePermission):
    def has_permission(self, request, view):

        # positionDoc = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        # if "automation" in positionDoc.desc:
        #     if "permission" in positionDoc.desc['automation']:
        #         perm = positionDoc.desc['automation']['permission']
        #         if perm.get("Sale_Manager") == True:
        #             return True
        #         if "Can_Work_With_Sale" in perm:
        #             return perm["Can_Work_With_Sale"]
        return True
