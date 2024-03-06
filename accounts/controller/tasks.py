from time import sleep
from accounts.models import BaseOrder


# TODO add condition here to if order allredy end job or turbo boosting order

def get_details(item_id):
    order = BaseOrder.objects.get(id=item_id)
    details = order.update_actual_price()
    return details
def update_database_task(item_id):
    delays = [60, 120 ,720 ,900]
    print(f"Updating database for item with ID: {item_id}")
    for delay in delays:
        sleep(delay)
        details = get_details(item_id)
        print(details, f'with delay {delay}')