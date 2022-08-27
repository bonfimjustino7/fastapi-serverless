import datetime
from typing import List, Literal

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class Payment(BaseModel):
    id: int
    type: Literal["pix", "credit_card"]
    status: Literal["paid", "unpaid"] = "unpaid"


class Invoice(BaseModel):
    payment: Payment
    status: Literal["paid", "unpaid", "past_due", "closure"] = "unpaid"
    due_date: datetime.date
    amount: float

    def past_due(self) -> bool:
        now = datetime.date.today()
        if now > self.due_date and self.payment.status == "unpaid":
            self.status = "past_due"

        return self.status == "past_due"

    def closure(self) -> bool:
        now = datetime.date.today()
        days = (self.due_date - now).days

        if (
            not self.status == "past_due"
            and days <= 7
            and self.payment.status == "unpaid"
        ):
            self.status = "closure"
            # create next invoice

        return self.status == "closure"

    def get_status(self) -> Literal["paid", "unpaid", "past_due", "closure"]:
        if self.past_due():
            return "past_due"
        if self.closure():
            return "closure"

        if self.payment.status == "paid":
            self.status = "paid"
            return self.status

        self.status = "unpaid"
        return self.status


class Subscription(BaseModel):
    user: User
    status: Literal["active", "inactive"]
    invoices: List[Invoice]
    amount: float
