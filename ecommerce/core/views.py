from django.shortcuts import render,redirect
from . models import Item,OrderItem,Order
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import CheckoutForm
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# def item_list(request):
#     context = {
#         'items':Item.objects.all()
#     }
#     return render(request,'home-page.html',context=context)


class ItemListView(ListView):
    model = Item
    template_name = 'home-page.html'
    context_object_name = 'items'


# class DetailItemView(DetailView):
#     model = Item
#     template_name = 'product-page.html'
    #queryset = Item.objects.all()

 #   def get_queryset(self):
 #       self.slug=

def detail_view(request,slug):
    obj = get_object_or_404(Item,slug=slug)
    context = {
        'obj':obj
    }
    return render(request,'product-page.html',context=context)

@login_required()
def add_to_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_item,created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order = order.items.add(order_item)
    else:
        ordered_date=timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('detail',slug=slug)

@login_required()
def remove_from_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
            messages.info(request, f"{item.title} quantity has updated.")
            return redirect("detail",slug=slug)
        else:
            messages.info(request, f"{item.title} quantity has updated.")
            return redirect("detail",slug=slug)

    else:
        messages.info(request, "You do not have an active order")
        return redirect("detail", slug=slug)


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            return render(self.request,'order_summary.html',context=context)
        except ObjectDoesNotExist:
            return redirect('/')


@login_required()
def add_to_order_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_item,created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        # else:
        #     order = order.items.add(order_item)

        # ordered_date=timezone.now()
        # order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        # order.items.add(order_item)
    return redirect('order_summary')


@login_required()
def remove_from_order_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                #order.orderitems.remove(order_item)
                order_item.delete()
            messages.info(request, f"{item.title} quantity has updated.")
            return redirect('order_summary')
        else:
        #     messages.info(request, f"{item.title} quantity has updated.")
             return redirect("order_summary")
    #
    # else:
    #     messages.info(request, "You do not have an active order")
    return redirect("order_summary")


class CheckoutView(View):
    def get(self, *args,**kwargs):
        form = CheckoutForm()
        context={
            'form':form
        }
        return render(self.request,'checkout-page.html', context=context)

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST)
        print(self.request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect('payment')
        print("failed checkout")
        return redirect('/')


# def payment(request):
#     return render(request,'payment.html')
class Payment(View):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

    def get(self,*args,**kwargs):
        return render(self.request,'payment.html')

    def post(self,*args,**kwargs):
        charge = stripe.Charge.create(
            amount=100,
            currency='usd',
            description='A Django charge',
            source=self.request.POST['stripeToken']
        )
        return render(self.request, 'payment.html')