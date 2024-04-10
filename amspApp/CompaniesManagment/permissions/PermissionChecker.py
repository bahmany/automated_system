from amspApp.CompaniesManagment.permissions.CompanyPermissions import IsOwnerOrReadOnly, CanCruid


def get_permissions(self, className):
    # Your logic should be all here
    if self.request.method == 'GET':
        self.permission_classes = [IsOwnerOrReadOnly, ]
    else:
        self.permission_classes = [CanCruid, ]

    return super(className, self).get_permissions()