# coding=utf-8

from django import forms
from djangular.styling.bootstrap3.forms import Bootstrap3Form
from amspApp.HRForms.models import HRSanadType, Vahed, Format, FarayandhayeMortabet, NoeSanad, HRForms, HRFormItems

__author__ = 'mohammad'





class HRFormsForm(Bootstrap3Form):
    # def __init__(self, *args, **kwargs):
    # super(Bootstrap3Form, self).__init__(*args, **kwargs)
    # self.helper = get_bootstrap_helper(
    #         list(self.Meta.fields),
    #         'save', 'Save'
    #     )


    # helper = FormHelper()
    # helper.layout = Layout(
    # Div(
    #         Div("code", css_class="col-xs-6"),
    #         Div("name", css_class="col-xs-6"),
    #         css_class="row-fluid")
    # )


    # zzz = forms.CharField(label="Hi", widget=DivForRub)

    code = forms.CharField(
        min_length=2,
        max_length=8,
        required=True,
        label="کد سند",
        help_text="این کد اختیاریست",
    )
    name = forms.CharField(
        min_length=5,
        max_length=100,
        required=True,
        label="عنوان فرم",
        help_text="لطفا عنوان فرم را وارد نمایید سعی کنید این عنوان منحصربفرد بوده و تکراری نباشد"
    )

    fileAddress = forms.FileField(
        allow_empty_file=False,
        # required=True,
        label="فایل پی دی اف",
        help_text="نوع فایل حتما می بایست pdf باشد",
        widget=forms.FileInput(attrs={
            "ngf-select": "",
            "ngf-multiple": "false",
            "accept": ".pdf",
            "ngf-drop": "",
            "ngf-drag-over-class": "{accept:'acceptClass', reject:'rejectClass', delay:100}|myDragOverClass|calcDragOverClass($event)",
            "ngf-drop-available": "dropSupported"
        })
    )

    HRSanadType = forms.ChoiceField(
        choices=[(x.id, x.name) for x in HRSanadType.objects.all().order_by("name")],
        required=True,
        label="نوع سند",  # foo, pr , ...
        help_text=""
    )
    Vahed = forms.ChoiceField(
        choices=[(x.id, x.name) for x in Vahed.objects.all().order_by("id")],
        required=True,
        label="واحد",  # foo, pr , ...
        help_text=""
    )
    Format = forms.ChoiceField(
        choices=[(x.id, x.name) for x in Format.objects.all().order_by("name")],
        required=True,
        label="فرمت",  # foo, pr , ...
        help_text=""
    )
    FarayandhayeMortabet = forms.ChoiceField(
        choices=[(x.id, x.name) for x in FarayandhayeMortabet.objects.all().order_by("name")],
        required=True,
        label="فرآیندهای مرتبط",  # foo, pr , ...
        help_text=""
    )
    NoeSanad = forms.ChoiceField(
        choices=[(x.id, x.name) for x in NoeSanad.objects.all().order_by("name")],
        required=True,
        label="مدل سند",  # foo, pr , ...
        help_text=""
    )


# def get_bootstrap_helper(fields, submit_id, submit_label):
# """ Return a crispy forms helper configured for a Bootstrap3 horizontal
# form.
#     """
#     helper = FormHelper()
#     helper.form_class = "form-horizontal"
#     helper.label_class = 'col-lg-4'
#     helper.field_class = 'col-lg-8'
#     fields.append(
#         Div(
#             Div(
#                 Submit(submit_id, submit_label, css_class='btn-default'),
#                 css_class='col-lg-offset-4 col-lg-8'
#             ),
#             css_class='form-group'
#         )
#     )
#     helper.layout = Layout(*fields)
#     return helper

#
# class HRFormsFormMix(NgModelFormMixin, NgFormValidationMixin, HRFormsForm):
#     # Apart from an additional mixin class, the Form declaration from the
#     # 'Classic Subscription' view, has been reused here.
#     # def __init__(self, *args, **kwargs):
#     #     super(HRFormsFormMix, self).__init__(*args, **kwargs)
#     #     setup_bootstrap_helpers(self)
#
#
#     pass

# def setup_bootstrap_helpers(object):
#     object.helper = FormHelper()
#     object.helper.form_class = 'form-horizontal'
#     object.helper.label_class = 'col-lg-3'
#     object.helper.field_class = 'col-lg-8'
