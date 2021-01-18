from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import  ListView, DetailView
from .forms import LoginForm, RegistrationForm
from .models import Customer, Goods, OrderLineItem, Orders
import random
import datetime

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            new_customer = Customer()
            new_customer.id = form.cleaned_data['userid']
            new_customer.name = form.cleaned_data['name']
            new_customer.password = form.cleaned_data['password1']
            new_customer.birthday = form.cleaned_data['birthday']
            new_customer.phone = form.cleaned_data['phone']

            new_customer.save()
            return render(request, 'customer_reg_success.html')

    else:
            form = RegistrationForm()

    return render(request, 'customer_reg.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            try:
                c = Customer.objects.get(id=userid)
            except:
                HttpResponseRedirect('login.html/')
            else:
                if c is not None and c.password == password:
                    request.session['customer_id'] = c.id
                    return HttpResponseRedirect('/main/')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def main(request):
    if not request.session.has_key('customer_id'):
        return HttpResponseRedirect('/login/')

    return render(request, 'main.html')


class GoodsListView(ListView):
    model = Goods
    ordering = ['id']
    #queryset =
    template_name = 'goods_list.html'

def show_goods_detail(request):
    goodsid = request.GET['id']
    try:
        g = Goods.objects.get(id=goodsid)
    except:
        HttpResponseRedirect('/list/')
    else:
       return render(request, 'goods_detail.html', {'goods': g})

def add_cart(request):
    if not request.session.has_key('customer_id'):
        return HttpResponseRedirect('/login/')

    goodsid = int(request.GET['id'])
    goodsname = request.GET['name']
    goodsprice = float(request.GET['price'])

    if not request.session.has_key('cart'):

        request.session['cart'] = []

    cart = request.session['cart']
    flag = 0
    for item in cart:
        if item[0] == goodsid:
            item[3] += 1
            flag = 1
            break

    if flag == 0:
        item = [goodsid, goodsname, goodsprice, 1]
        cart.append(item)

    request.session['cart'] = cart

    page = request.GET['page']
    if page == 'detail':
        return HttpResponseRedirect('/detail/?id=' + str(goodsid))
    else:
        return HttpResponseRedirect('/list/')


def show_cart(request):
    if not request.session.has_key('customer_id'):
        return HttpResponseRedirect('/login/')
    if not request.session.has_key('cart'):
        return render(request, 'cart.html', {'list': [], 'total': 0.0})

    cart = request.session['cart']

    list = []
    total = 0.0
    for item in cart:
        # item [商品id，商品名称，价格，数量]
        subtotal = item[2] * item[3]
        total += subtotal

        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)

    return render(request, 'cart.html', {'list': list, 'total': total})

def submit_orders(request):
    if request.method == 'POST':
        orders = Orders()
        n = random.randint(0,9)
        d = datetime.datetime.today()
        orders.id = str(int(d.timestamp() * 1e6)) + str(n)
        orders.order_date = d
        orders.status = 1
        orders.total = 0
        orders.save()

        cart = request.session['cart']
        total = 0.0

        for item in cart:
            goodsid = item[0]
            goods = Goods.objects.get(id=goodsid)

            quantity = request.POST['quantity_' + str(goodsid)]

            try:
                quantity = int(quantity)
            except:
                quantity = 0

            subtotal = item[2] * quantity
            total += subtotal

            order_line_item = OrderLineItem()
            order_line_item.quantity = quantity
            order_line_item.goods = goods
            order_line_item.orders = orders
            order_line_item.total = subtotal
            order_line_item.save()

        orders.total = total
        orders.save()

        del request.session['cart']

        return render(request, 'order_finish.html', {'ordersid': orders.id})

def logout(request):
    if not request.session.has_key('customer_id'):
        del request.session['customer_id']
        if not request.session.has_key('cart'):
            del request.session['cart']
    return HttpResponseRedirect('/login/')