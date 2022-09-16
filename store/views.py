from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import datetime
from .utils import CookieCart , CartData , guestOrder
# Create your views here.
from django.template.loader import render_to_string

from store.models import Product, Order, OrderItem, ShippingAddress, Customer
import json

def store(request):
    products = Product.objects.all()
    order , created =  Order.objects.get_or_create(customer_id=request.user.id , complete=False)

    context = {'products' : products , 'order_items':order.orderitem_set.count()}
    return render(request , 'store/store.html' , context)



def cart(request):
    context = CartData(request)
    return render(request, 'store/cart.html', context)







def checkout(request):
    context = CartData(request)
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    product = Product.objects.filter(id=product_id).first()
    if product is not None:
        customer = request.user.customer
        order , created = Order.objects.prefetch_related('orderitem_set').get_or_create(customer_id=customer.id , complete=False)
        orderitem , created = OrderItem.objects.get_or_create(order_id=order.id , product_id=product_id )
        if action == 'add':
                orderitem.quantity +=1
                orderitem.save()
        else:
            if orderitem.quantity <= 1:
                orderitem.delete()
            else:
                orderitem.quantity -= 1
                orderitem.save()

    else:
        return JsonResponse({
            'status': 'product_not_found'
        })
    order, created = Order.objects.prefetch_related('orderitem_set').get_or_create(customer_id=customer.id,complete=False)
    order_item = order.orderitem_set.count()
    page_cart = render_to_string('store/order_item.html', context={'order': order})
    return JsonResponse({'page_cart':page_cart , 'order_items':order_item})



def ProcessOrder(request):
    data = json.loads(request.body)
    transection_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer_id=customer.id,complete=False)
    else:
        order , customer = guestOrder(request , data)

    print(float(data['user_info']["total"]))
    print(order.get_cart_total)
    print(float(data['user_info']["total"]) == order.get_cart_total)
    if float(data['user_info']["total"]) == float(order.get_cart_total):
        print("HGKJ")
        order.complete = True
    order.transection_id = transection_id
    order.save()
    if order.shipping:
        address = data['user_shipping']["address"]
        city = data['user_shipping']["city"]
        state = data['user_shipping']["state"]
        zipcode = data['user_shipping']["zipcode"]
        ShippingAddress.objects.create(customer_id=customer.id, order_id=order.id, address=address, city=city,zipcode=zipcode, state=state)
    return JsonResponse({"status": "OK"})


def site_header(request):
    if request.user.is_authenticated:
        order_items = Order.objects.filter(customer_id=request.user.customer , complete=False).first().orderitem_set.count()
    else:
        order_items = CookieCart(request)['order']['get_order_item_count']
    context = {
        'order_items': order_items
    }
    return render(request , 'shared/includes/site_header.html' , context)


