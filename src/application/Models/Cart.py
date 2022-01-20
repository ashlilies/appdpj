# Ashlee
# Shopping cart system, to be used in Consumer accounts

class Cart:
    def __init__(self):
        self.__item_quantity_dict = {}  # key: item_id, value: quantity

    def add_item(self, item_id: int):
        if item_id in self.__item_quantity_dict:
            self.__item_quantity_dict[item_id] += 1
        else:
            self.__item_quantity_dict[item_id] = 1

    def remove_item(self, item_id: int, quantity: int = 1):
        if item_id in self.__item_quantity_dict:
            if self.__item_quantity_dict[item_id] > 1:
                self.__item_quantity_dict[item_id] -= quantity
            else:
                self.__item_quantity_dict.pop(item_id)

    def get_item_ids(self) -> list:
        item_ids = []
        for item_id in self.__item_quantity_dict:
            item_ids.append(item_id)
        return item_ids

    def clear_cart(self):
        for item_id in self.__item_quantity_dict:
            self.__item_quantity_dict.pop(item_id)