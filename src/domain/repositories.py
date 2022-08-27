from abc import ABC, abstractmethod

from domain.entities import Invoice, Subscription


class SubscriptionRepository(ABC):
    @abstractmethod
    def create(self, subscription: Subscription):
        raise NotImplementedError


class InvoiceRepository(ABC):
    @abstractmethod
    def create(self, invoice: Invoice):
        raise NotImplementedError

    @abstractmethod
    def create_next_invoice(self, previous_invoice: Invoice):
        raise NotImplementedError
