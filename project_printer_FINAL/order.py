class Order:
    """
    Class to represent an order containing multiple order items.
    """
    def __init__(self, order_id, company_id):
        self.order_id = order_id  # Order ID
        self.company_id = company_id  # Company ID
        self.items = []  # List to hold OrderItem objects

    def add_item(self, item):
        """
        Adds an OrderItem to the order.
        """
        self.items.append(item)

    def __str__(self):
        """
        String representation of the Order object.
        """
        return f"Order(order_id={self.order_id}, company_id={self.company_id}, items={[str(item) for item in self.items]})"

class OrderItem(Order):
    """
    Class to represent an order item.
    """
    def __init__(self, order_id, company_id, design_id, file_name, file_path, qty, pk_qty, total_qty, edit_url):
        super().__init__(order_id, company_id)  # Inherit order_id and company_id from Order class
        self.design_id = design_id  # Design ID
        self.file_name = file_name  # File name
        self.file_path = file_path  # File path
        self.qty = qty  # Quantity of items
        self.pk_qty = pk_qty  # Quantity per pack
        self.total_qty = total_qty  # Total quantity
        self.edit_url = edit_url  # Edit url

    def __str__(self):
        """
        String representation of the OrderItem object.
        """
        return f"OrderItem(design_id={self.design_id}, file_name={self.file_name}, file_path={self.file_path}, qty={self.qty}, pk_qty={self.pk_qty}, total_qty={self.total_qty}, edit_url={self.edit_url})"
