from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.Infrustructures.Classes.DateConvertors import get_date_str, PrettyDayShow, sh_to_mil, mil_to_sh, \
    mil_to_sh_with_time
from amspApp.Sales.models import MojoodiGhabeleForoosh, MojoodiGhabeleForooshKeifi
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class MojoodiGhabeleForooshSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = MojoodiGhabeleForoosh

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def to_representation(self, instance):
        result = super(MojoodiGhabeleForooshSerializer, self).to_representation(instance)
        result['keifi'] = MojoodiGhabeleForooshKeifi.objects.filter(
            HavalehForooshApproveLink=instance.id
        )
        result['keifi'] = MojoodiGhabeleForooshKeifiSerializer(instance=result['keifi'], many=True).data
        return result


class MojoodiGhabeleForooshKeifiSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = MojoodiGhabeleForooshKeifi
        depth = 1

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def to_representation(self, instance):
        result = super(MojoodiGhabeleForooshKeifiSerializer, self).to_representation(instance)
        result['user'] = PositionsDocument.objects.filter(positionID=instance.positionID).first()
        result['dateof'] = get_date_str(instance.dateOfPost)
        result['dateof_pretty'] = PrettyDayShow(instance.dateOfPost)
        result['dateof_sh'] = mil_to_sh_with_time(instance.dateOfPost)
        result['user'] = {
            'profileName': result['user'].profileName,
            'chartName': result['user'].chartName,
            'avatar': result['user'].avatar,

        }
        return result
