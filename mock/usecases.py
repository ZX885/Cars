from django.contrib import messages
from cars.models import Cars

WISH_LIST = 'wish-list'
VIEWED_CARS = 'viewed-cars'
CAR_IDS = "car_id"


class Session:
    valid_keys = [WISH_LIST,VIEWED_CARS]

    def __init__(self, request) -> None:
        self.session = request.session

    def get(self, key: str, default=None):
        """
        Gets item(s) from session storage
        or gives default value
        """
        self._check_key(key)
        value = self.session.get(key, default)
        return value

    def set(self, key: str, value) -> None:
        """
        CAUTION: This method will override everything
        RU: Этот метод перезапишет всё
        """
        self._check_key(key)
        self.session[key] = value

    def update(self, key: str, value) -> None:
        raise NotImplementedError

    def _check_key(self, key: str) -> bool:
        if key not in self.valid_keys:
            # {key=}  =>  key=...
            raise KeyError(f"{key=} is not a valid key")
        return True


def send_to_buy(request, item_id: int, obj_name: str) -> None:
    """Sends item to wishlist

    Args:
        request (HttpRequest): needed to get session 
        item_id (int): id of any item
        obj_name (str): name of object (book, etc.)
    """
    session = Session(request)
    wish_list = session.get(WISH_LIST, {})

    match obj_name:
        case "car":
            if wish_list.get(CAR_IDS):
                if item_id in wish_list[CAR_IDS]:
                    return True
                wish_list[CAR_IDS].append(item_id)
            else:
                wish_list[CAR_IDS] = [item_id]
            session.set(WISH_LIST, wish_list)

#     # We can add more objects here
#     pass


def getItemsFromWishlist(request, item_type: str = 'all') -> list[int]:
    """
        Gets items from wishlist (all by default or by type)
    """
    session = Session(request)
    wish_list = session.get(WISH_LIST, {})

    match item_type:
        case "all":
            return wish_list
        case "car":
            return wish_list.get(CAR_IDS, [])

    # We can add more logic here
    pass


def delete_item_from_wishlist(request, item_id: int, item_type: str) -> None:
    session = Session(request)
    wish_list = session.get(WISH_LIST, {})

    match item_type:
        case "book":
            cars_ids = wish_list.get(CAR_IDS)
            cars_ids.remove(item_id)
            wish_list[CAR_IDS] = cars_ids

    session.set(WISH_LIST, wish_list)
