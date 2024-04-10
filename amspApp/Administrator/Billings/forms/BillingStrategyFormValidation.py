from djangular.forms import NgModelFormMixin, NgFormValidationMixin
from amspApp.Administrator.Billings.forms.BillingStrategyForm import BillingStrategyForm
from amspApp.Administrator.Customers.forms.PaymentForm import PaymentForm


class BillingStrategyForm(NgModelFormMixin, NgFormValidationMixin, BillingStrategyForm):

    # Apart from an additional mixin class, the Form declaration from the
    # 'Classic Subscription' view, has been reused here.
    pass

class PaymentForm(NgModelFormMixin, NgFormValidationMixin, PaymentForm):

    # Apart from an additional mixin class, the Form declaration from the
    # 'Classic Subscription' view, has been reused here.
    pass
