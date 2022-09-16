from .models import *
import json



def CookieCart(request):
    try:
        cookie = json.loads(request.COOKIES['cart'])
    except:
        cookie = {}
    order_items = []
    order = {'get_order_item_count': len(order_items), 'get_cart_total': 0, 'shipping': False}
    for product_id in cookie:
        product = Product.objects.filter(id=product_id).first()
        if product is not None:
            order_item = {
                'product': {
                    'id': product.id,
                    'image': product.image,
                    'price': product.price,
                    'name': product.name
                },
                'get_product_total': product.price * cookie[product_id]['quantity'],
                'quantity': cookie[product_id]['quantity']
            }
            order['get_cart_total'] += product.price * cookie[product_id]['quantity']
            order_items.append(order_item)

            if product.digital == False:
                order['shipping'] = True

    order['get_order_item_count'] = len(order_items)

    return {'order':order , 'items' : order_items}



def CartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.prefetch_related('orderitem_set').get_or_create(customer=customer,complete=False)
        context = {'order': order, 'items': order.orderitem_set.all}
    else:
        context = CookieCart(request)

    return context

def guestOrder(request , data):
    name = data['user_info']['name']
    email = data['user_info']['email']
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer_id=customer.id, complete=False)

    items = CookieCart(request)['items']
    for item in items:
        OrderItem.objects.create(product_id=item['product']['id'], order_id=order.id,quantity=item['quantity'])

    return order , customer