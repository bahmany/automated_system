from djangular.forms import NgModelFormMixin, NgFormValidationMixin
from amspApp.Administrator.Customers.forms.CustomerRegisterForm import CustomerRegistrationForm


class CustomerRegistrationForm(NgModelFormMixin, NgFormValidationMixin, CustomerRegistrationForm):

    # Apart from an additional mixin class, the Form declaration from the
    # 'Classic Subscription' view, has been reused here.
    pass
