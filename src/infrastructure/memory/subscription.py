from domain.entities import Subscription
from domain.repositories import SubscriptionRepository


class SubscriptionMemoryRepository(SubscriptionRepository):
    def create(self, subscription: Subscription):
        data = subscription.json()
        print("\n" + data)
