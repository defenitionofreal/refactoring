from .repos import *


class NotExistingSearchException(Exception):
    def __init__(self, message="Search does not exists."):
        self.message = message
        super().__init__(self.message)


class OrderListValidator:
    def __init__(self, user_id: int):
        self._repo = OrderListRepo(user_id)

    def _validate_existing_search(self):
        if not self._repo.is_existing_search():
            raise NotExistingSearchException()

    def validate(self):
        self._validate_existing_search()


class CostListValidator:
    def __init__(self, user_id: int):
        self._repo = CostListRepo(user_id)

    def _validate_existing_search(self):
        if not self._repo.is_existing_search():
            raise NotExistingSearchException()

    def validate(self):
        self._validate_existing_search()
