import stripe
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from DocShop import settings
from store.forms import OrderForm
from store.models import Product, Cart, Order

stripe.api_key = settings.STRIPE_API_KEY

def index(request):
    products = Product.objects.all()

    return render(request, 'store/index.html', context={"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product": product})

def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"slug": slug}))


def cart(request):
    orders = Order.objects.filter(user=request.user)
    if orders.count() == 0:
        return redirect("index")
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(queryset=orders)

    return render(request, 'store/cart.html', context={"forms": formset})

def update_quantities(request):
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(request.POST,queryset=Order.objects.filter(user=request.user))
    if formset.is_valid():
        formset.save()

    return redirect('cart')

def create_checkout_session(request):
    cart = request.user.cart

    line_items = [{"price": order.product.stripe_id,
                   "quantity": order.quantity} for order in cart.orders.all()]

    session = stripe.checkout.Session.create(
        locale="fr",
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        customer_email = request.user.email,
        success_url=request.build_absolute_uri(reverse('checkout-success')),
        cancel_url='http://127.0.0.1:8000/',
    )

    return redirect(session.url, code=303)

def checkout_success(request):
    return render(request,'store/success.html')

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()

    return redirect('index')
