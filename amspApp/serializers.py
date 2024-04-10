from amspApp._Share.DynamicFieldModelSerializer import DynamicFieldsModelSerializer
from amspApp.models import Helpbar


class HelpbarSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Helpbar

