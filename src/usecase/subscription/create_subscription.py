from abc import ABC, abstractmethod

from domain.entities import Invoice, Subscription, User
from domain.repositories import SubscriptionRepository


class SubscriptionCommandUseCaseGeneric(ABC):
    @abstractmethod
    def handle(self, user: User, invoice: Invoice, amount: float):
        raise NotImplementedError


class CreateSubscriptionHandle(SubscriptionCommandUseCaseGeneric):
    def __init__(self, subscription_repository: SubscriptionRepository):
        self._subscription_repository = subscription_repository

    def handle(self, user: User, invoice: Invoice, amount: float) -> Subscription:
        status = "active" if invoice.get_status() == "paid" else "inactive"
        sub = Subscription(user=user, status=status, invoices=[invoice], amount=amount)
        self._subscription_repository.create(sub)

        return sub
