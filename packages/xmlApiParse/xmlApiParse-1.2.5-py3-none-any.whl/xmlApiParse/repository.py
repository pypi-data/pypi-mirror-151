from typing import TypedDict


class EmployeeDTO(TypedDict):
    restaurant: str
    name: str
    altname: str
    role: str
    gen_san_date: str
    gen_tax_payer_id_num: str
    ident: int


class OrderListDTO(TypedDict):
    order_id: int
    order_name: str
    url: str
    version: int
    crc32: int
    guid: set
    table_id: int
    table_code: int
    order_categ_id: int
    order_categ_code: int
    order_type_id: int
    order_type_code: int
    waiter_id: int
    waiter_code: int
    order_sum: int
    to_pay_sum: int
    price_list_sum: int
    total_pieces: int
    finished: int
    bill: int
    dessert: int


class WaiterListDTO(TypedDict):
    id: int
    code: int


class RestaurantsDTO(TypedDict):
    name: str
    alt_name: str
    ident: int


class MenuDTO(TypedDict):
    ident: int
    price: int


class MenuItemsDTO(TypedDict):
    ident: int
    item_ident: int
    source_ident: int
    guid_string: set
    assign_childs_on_server: bool
    active_hierarchy: bool
    code: int
    name: str
    alt_name: str
    main_parent_ident: int
    status: str
    sales_terms_start_sale: int
    sales_terms_stop_sale: int
    future_tax_dish_type: int
    parent: int
    cook_mins: int
    modi_weight: int
    min_rest_qnt: int
    categ_path: str
    price_mode: str
    modi_scheme: int
    combo_scheme: int


class WaiterDTO(TypedDict):
    restaurant: str
    name: str
    ident: int
    code: int


class ConnectionErrors(Exception):
    pass


class ParseError(Exception):
    pass


class BadRequestError(Exception):
    pass
