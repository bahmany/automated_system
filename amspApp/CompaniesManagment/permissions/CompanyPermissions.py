from rest_framework import permissions

from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.views.CompaniesManagmentView import CompaniesManagmentViewSet


# class CanCruid(permissions.BasePermission):
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
class CanCruid(permissions.BasePermission):

    def has_permission(self, request, view):
        currentCompanyInstance = view.request.user.current_company
        # currentCompanyInstance = Company.objects.get(id=int(view.kwargs["companyID_id"]))

        if 'post' in view.action_map:
            if view.action_map['post'] == "ChangeDefault":
                # checking if this person has permission in the selected company
                countPermission = Position.objects.filter(company = currentCompanyInstance.id, user = request.user.id).count()
                if countPermission != 0:
                    return True
                else:
                    return False


        if "id" in request.query_params:
            currentCompanyInstance = Company.objects.get(id = int(request.query_params["id"]))
        if "companyID_id" in view.kwargs:
            if view.kwargs["companyID_id"] != "undefined":
                currentCompanyInstance = Company.objects.get(id=int(view.kwargs["companyID_id"]))
        if currentCompanyInstance == None:
            return False
        userID = request.user.id
        res = CompaniesManagmentViewSet().getUserCompanyPermission(userID, currentCompanyInstance)
        for r in res:
            if r[0] == view.permission_name:
                return True
        # i have to set special access to clients api
        # if client has permission to start a process
        if view.action_map.get("get") == "listForStart":
            return True
        if request.user.groups.all().filter(name='edari_manager').count() > 0:
            return True





        return False




