import uuid
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import update_session_auth_hash
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from amspApp.CompaniesManagment.serializers.CompanySerializers import CompanySerializer
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from amspApp.amspUser.models import MyUser, positionIDLastActivities, FirstReg, ForgetPassCodes, BasicAuths


class UserNameSerializer(serializers.HyperlinkedModelSerializer):
    name = ProfileSerializer(read_only=True, )

    class Meta:
        model = MyUser
        fields = ("id", "username", "name")

class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        style={'template': 'forms/base-templates/textarea.html', 'cssclass': 'col-md-12', 'ngmodel': 'user.username'},
        label='username',
        validators=[UniqueValidator(queryset=MyUser.objects.all()), RegexValidator(r'^[-a-zA-Z0-9_]+$',
                                                                                   'Enter a valid username. '
                                                                                   'This value may contain only letters, numbers '
                                                                                   'and - and _ characters.',
                                                                                   'invalid')])
    email = serializers.EmailField(
        style={'template': 'forms/base-templates/textarea.html', 'cssclass': 'col-md-12', 'ngmodel': 'user.email'},
        label='email', validators=[UniqueValidator(queryset=MyUser.objects.all())])

    password = serializers.CharField(min_length=3, required=False, write_only=True,
                                     style={'template': 'forms/base-templates/password.html', 'cssclass': 'col-md-12',
                                            'ngmodel': 'user.password'}, label='password')
    confirm_password = serializers.CharField(write_only=True, required=False, min_length=3,
                                             style={'template': 'forms/base-templates/password.html',
                                                    'cssclass': 'col-md-12',
                                                    'ngmodel': 'user.confirm_password'}, label='confirm_password')

    user_permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(),
                                                          required=False,
                                                          style={
                                                              'template': 'forms/base-templates/select_multiple.html',
                                                              'cssclass': 'col-md-12',
                                                              'ngmodel': 'user.user_permissions',
                                                              'searchFunc': 'searchPermissions()',
                                                              'searchInput': 'permissionSearchInput',
                                                              'options': 'permissionOptions', 'dataname': 'name'},
                                                          label='permissions', )

    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(),
                                                required=False,
                                                style={'template': 'forms/base-templates/select_multiple.html',
                                                       'cssclass': 'col-md-12', 'ngmodel': 'user.groups',
                                                       'searchFunc': 'searchPermissions()',
                                                       'searchInput': 'groupSearchInput',
                                                       'options': 'groupOptions', 'dataname': 'name'},
                                                label='groups', )

    class Meta:
        model = MyUser
        fields = (
            'id',
            'email',
            'username',
            'password',
            'confirm_password',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'account_type',
            'cellphone',
            'personnel_code',
            'user_permissions')

    def validate(self, data):

        if 'password' in data and 'confirm_password' in data and data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"status": "Bad request", "message": {"confirm_password": ["passwords not match"]}})
        return data

    def create(self, validated_data):
        if validated_data.get('password', None):
            pass
        else:
            raise serializers.ValidationError(
                {"status": "Bad request", "message": {"password": ["This field is required"]}})
        if validated_data.get('confirm_password', None):
            pass
        else:
            raise serializers.ValidationError(
                {"status": "Bad request", "message": {"confirm_password": ["This field is required"]}})
        del validated_data["confirm_password"]
        newUser = MyUser(**validated_data)
        newUser.set_password(validated_data["password"])
        newUser.is_staff = True

        # newUser = MyUser.objects.create_user(**validated_data)
        # newUser.customerID = companyID
        newUser.save()
        ProfileSerializer().create_default_profile(newUser)

        # this def creates a default company for new user
        CompanySerializer().create_default_company_from_user(newUser)

        # adding default fileFolder
        newFileFolder = {
            'userID': newUser.id,
            'name': "Root Folder",
            'parentFolder': 0,
            'privacy': 1,
        }
        from amspApp.FileServer.serializers.FileFolderSerializer import FileFoldersSerializers
        newFolder = FileFoldersSerializers(data=newFileFolder)
        newFolder.is_valid(raise_exception=True)
        newFolder.save()

        return newUser

    # comment
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.groups = validated_data.get('groups', instance.groups)
        instance.user_permissions = validated_data.get('user_permissions', instance.user_permissions)
        if 'action' in self.initial_data and self.initial_data['action'] == 'passive/active':
            if instance.is_active:
                instance.is_active = False
            else:
                instance.is_active = True
        if 'action' in self.initial_data and self.initial_data['action'] == 'delete':
            instance.username = "%s.%s" % (uuid.uuid4(), validated_data.get('username', instance.username))
            instance.email = "%s.%s" % (uuid.uuid4(), validated_data.get('email', instance.email))
            instance.is_active = False
            instance.is_staff = False
            instance.is_superuser = False
            instance.is_deleted = True
        instance.save()
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()
        update_session_auth_hash(self.context.get('request'), instance)
        return instance


class positionIDLastActivitiesSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = positionIDLastActivities

    depth = 1


class FirstRegSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = FirstReg

    depth = 1


class ForgetPassCodesSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = ForgetPassCodes



    depth = 1


class BasicAuthsSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = BasicAuths
