from typing import Optional, Type


class TreeElem:
    child_cls: Type["TreeElem"]

    def __init__(self, name, parent: Optional["TreeElem"] = None):
        self.name = name
        self.__parent = parent
        self.__childs = dict()

    def _create_child(self, name):
        child = self.child_cls(name, parent=self)
        self.__childs[name] = child
        return child

    def _get_child(self, name):
        return self.__childs[name]

    def _get_all_childs(self):
        return self.__childs

    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}: {len(self._get_all_childs())} childs"


class ProductType:
    def __init__(self, name, parent: Optional["ChildCategory"] = None):
        self.name = name
        self.parent = parent

    def __str__(self):
        return f"Тип товара: {self.parent.name} - {self.name}"


class ChildCategory(TreeElem):
    child_cls = ProductType

    def get_all_products_types(self):
        return super()._get_all_childs()

    def get_product_type(self, name):
        return super()._get_child(name)

    def create_product_type(self, name):
        return super()._create_child(name)


class ParentCategory(TreeElem):
    child_cls = ChildCategory

    def get_all_child_categories(self):
        return super()._get_all_childs()

    def get_child_category(self, name):
        return super()._get_child(name)

    def create_child_category(self, name):
        return super()._create_child(name)


class Tree(TreeElem):
    child_cls = ParentCategory

    def get_all_parent_categories(self):
        return super()._get_all_childs()

    def get_parent_category(self, name):
        return super()._get_child(name)

    def create_parent_category(self, name):
        return super()._create_child(name)
