from djangular.styling.bootstrap3.forms import Bootstrap3ModelForm
from django import forms
from amspApp.Administrator.Billings.models import Billing_Strategies

__author__ = 'mohammad'




"""
    TypeOfBilling = models.IntegerField(default=2)
    startDate = models.DateTimeField(default=datetime.now(), blank=True)
    endDate = models.DateTimeField(default=datetime.now(), blank=True)
    days = models.IntegerField(default=-1)
    daysOfTrial = models.IntegerField(default=30)
    StorageMb = models.IntegerField(default=10240)
    CostPerUser = models.BigIntegerField(default=750000) # rial


"""

class BillingStrategyForm(Bootstrap3ModelForm):
    Title = forms.CharField(
        min_length=2,
        max_length=600,
        required=True,
        label="عنوان",
        help_text="عنوان استراتژی پرداخت برای فراخوانی ها"
    )
    TypeOfBilling = forms.ChoiceField(
        required=True,
        label="نوع پرداخت",
        help_text="نوع پرداخت نمایان کننده ی نحوه و زمان پرداخت هاست",
        choices=Billing_Strategies().Billing_Stat_Choices,
        widget = forms.Select
    )
    days = forms.IntegerField(
        required=False,
        label="تعداد روزها",
        help_text="تعداد روزها در نوع پرداخت تعداد روز نیاز است"
    )
    daysOfTrial = forms.IntegerField(
        required=False,
        label="تعداد روزهای آزمایشی",
        help_text="تعداد روزهایی کاربر می تواند هزینه ی خود را پس گیرد"
    )
    StorageMb = forms.IntegerField(
        required=False,
        label="فضای درخواستی",
        help_text="فضای درخواستی به مگابایت است",
    )

    CostPerUser = forms.IntegerField(
        required=True,
        label="هزینه ی دریافتی",
        help_text="فضای درخواستی به مگابایت است",
    )

    exp = forms.CharField(
        min_length=2,
        max_length=600,
        required=False,
        label="سایر توضیحات",
        help_text="اطلاعات مورد نیاز را در این قسمت وارد نمایید"
    )

    def __init__(self, *args, **kw):
        super(BillingStrategyForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'TypeOfBilling',
            'days',
            'daysOfTrial',
            'StorageMb',
            'CostPerUser',
            'exp'
        ]

    class Meta:
        model = Billing_Strategies
        fields = '__all__'
        exclude = ['createdUserID', 'dateOfPost', 'isDeleted', 'isPublished']




