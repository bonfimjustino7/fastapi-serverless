import datetime
from unittest import mock

from domain.entities import Invoice, Payment, Subscription, User
from infrastructure.memory.subscription import SubscriptionMemoryRepository
from usecase.subscription.create_subscription import CreateSubscriptionHandle


class StubDate(datetime.date):
    pass


def create_subscription() -> Subscription:
    repo = SubscriptionMemoryRepository()
    use_case = CreateSubscriptionHandle(repo)

    user = User(id="123", name="Jonh Teste")
    payment = Payment(id="1212921", type="pix")
    invoice = Invoice(
        payment=payment, due_date=datetime.date(2022, 8, 20), amount=100.0
    )
    subscription = use_case.handle(user, invoice, invoice.amount)
    return subscription


@mock.patch("domain.entities.datetime.date", StubDate)
def test_create_subscription():

    StubDate.today = classmethod(lambda cls: datetime.date(2022, 3, 30))

    subscription = create_subscription()
    invoice = subscription.invoices[0]
    payment = invoice.payment

    assert isinstance(subscription, Subscription)

    assert len(subscription.invoices) == 1

    assert (
        subscription.status == "inactive"
        and invoice.status == "unpaid"
        and payment.status == "unpaid"
    )


def test_create_subscription_past_due():
    subscription = create_subscription()
    invoice = subscription.invoices[0]
    payment = invoice.payment

    assert isinstance(subscription, Subscription)

    assert len(subscription.invoices) == 1
    assert (
        subscription.status == "inactive"
        and invoice.status == "past_due"
        and payment.status == "unpaid"
    )


@mock.patch("domain.entities.datetime.date", StubDate)
def test_create_subscription_closure():

    StubDate.today = classmethod(
        lambda cls: datetime.date(2022, 8, 20)
    )  # - past_due: 2022, 8, 20 =

    subscription = create_subscription()
    invoice = subscription.invoices[0]
    payment = invoice.payment

    assert isinstance(subscription, Subscription)

    assert len(subscription.invoices) == 1

    assert (
        subscription.status == "inactive"
        and invoice.status == "closure"
        and payment.status == "unpaid"
    )
