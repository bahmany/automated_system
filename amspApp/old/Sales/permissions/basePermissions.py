from rest_framework import permissions

from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class CanCruidSale(permissions.BasePermission):
    def has_permission(self, request, view):
        if (not (request.user.is_active)):
            return False

        if request._request.path == '/page/sales/':
            if request.user.groups.all().filter(name='group_extis_permited_to_view').count() == 1:
                return True
        if request._request.path == '/page/Khorooj/':
            if request.user.groups.all().filter(name='group_extis_permited_to_view').count() == 1:
                return True
        if request._request.path == '/page/KhoroojDetails/':
            if request.user.groups.all().filter(name='group_extis_permited_to_view').count() == 1:
                return True
        if request._request.path == '/page/showSignBodyPrc/':
            if request.user.groups.all().filter(name='group_extis_permited_to_view').count() == 1:
                return True
        if request._request.path == '/page/signExit/':
            if request.user.groups.all().filter(name='group_extis_permited_to_view').count() == 1:
                return True

        positionDoc = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        if "automation" in positionDoc.desc:
            if "permission" in positionDoc.desc['automation']:
                perm = positionDoc.desc['automation']['permission']
                if perm.get("Sale_Manager") == True:
                    return True
                if "Can_Work_With_Sale" in perm:
                    return perm["Can_Work_With_Sale"]
        return False


class AllAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class IsHeSalePerson(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if request.user.groups.all().filter(name='foroosh').count() != 0:
                return True
        return False
