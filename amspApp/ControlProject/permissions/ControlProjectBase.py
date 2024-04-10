from rest_framework import permissions

from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class IsOwnerOrReadOnly_CostCol(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        positionDoc = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        if "automation" in positionDoc.desc:
            if "permission" in positionDoc.desc['automation']:
                perm = positionDoc.desc['automation']['permission']
                if perm.get("Sale_Manager") == True:
                    return True



        if request.method in permissions.SAFE_METHODS:
            return True
        current = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        return obj.positionID == current.positionID