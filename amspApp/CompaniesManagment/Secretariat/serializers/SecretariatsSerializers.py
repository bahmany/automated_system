from rest_framework import serializers
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.CompaniesManagment.Secretariat.models import Secretariat, SecretariatPermissions
from amspApp.CompaniesManagment.models import Company


class SecretariatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretariat



    '''
    checking secretariat permissions to allow create letter types or not

    '''
    def CheckPermission(self, letterObj):
        if letterObj['letterType'] == 1:
            if letterObj['secretariatPermission']['permission'][0] == '0':
                raise Exception("Not allow to use this secretariat")
        if letterObj['letterType'] == 2:
            if letterObj['secretariatPermission']['permission'][0] == '0':
                raise Exception("Not allow to use this secretariat")
        if letterObj['letterType'] == 3:
            if letterObj['secretariatPermission']['permission'][0] == '0':
                raise Exception("Not allow to use this secretariat")


    '''
    this def is for checking if position has default secretriat
    if there is no one
    this func creates default one
    '''
    def getDefaultSec(self, userID, companyID, positionDict = {}):
        mustUpdate = False

        if positionDict == {}:
            mustUpdate = True

        if not 'defaultSec' in positionDict:
            mustUpdate = True

        if positionDict['defaultSec'] == None:
            mustUpdate = True

        if mustUpdate:
            posDocInstance = PositionsDocument.objects.get(
                userID = userID,
                companyID = companyID,
            )
            secInstance = Secretariat.objects.filter(company = companyID)[0]
            posDocPartial = PositionDocumentSerializer(instance=posDocInstance, data={"defaultSec":secInstance.id}, partial=True)
            posDocPartial.is_valid(raise_exception=True)
            posDocPartial = posDocPartial.update(secInstance, posDocPartial.validated_data)
            return posDocPartial.id


        return positionDict['defaultSec']




class SecretariatSerializerPermission(serializers.ModelSerializer):
    class Meta:
        model = SecretariatPermissions



