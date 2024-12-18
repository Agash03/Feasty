from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

#menu view
class Home(LoginRequiredMixin,View):
    
    login_url = '/'
    
    def get(self, request):
        nvmenu_item = NonVegMenu.objects.all()[:3]
        vegmenu_item = VegMenu.objects.all()[:3]
        
        context = {
            'nvmenu_item': nvmenu_item,
            'vegmenu_item': vegmenu_item
     }
        return render(request, 'home.html', context)

    def post(self, request):
        nvmenu_item = NonVegMenu.objects.all()
        vegmenu_item = VegMenu.objects.all()
        
        context = {
            'nvmenu_item': nvmenu_item,
            'vegmenu_item': vegmenu_item
        }
        return render(request, 'home.html', context)


class VeganMenu(LoginRequiredMixin, View):
    login_url = '/'
    
    def get(self, request):
        vegmenu_items = VegMenu.objects.all()
        
        # Group items by food type
        menu_sections = {}
        for item in vegmenu_items:
            if item.food_type not in menu_sections:
                menu_sections[item.food_type] = []
            menu_sections[item.food_type].append(item)
        
        # Convert dictionary to list for easy iteration in template
        v_menu_sections_list = [{'id': key, 'name': key.capitalize(), 'items': items} for key, items in menu_sections.items()]
        
        context = {
            'menu_sections': v_menu_sections_list
        }
        return render(request, 'vegmenu.html', context)

class NVMenu(LoginRequiredMixin, View):
    login_url = '/'
    
    def get(self, request):
        nvmenu_items = NonVegMenu.objects.all()
        
        # Group items by food type
        menu_sections = {}
        for item in nvmenu_items:
            if item.food_type not in menu_sections:
                menu_sections[item.food_type] = []
            menu_sections[item.food_type].append(item)
        
        # Convert dictionary to list for easy iteration in template
        menu_sections_list = [{'id': key, 'name': key.capitalize(), 'items': items} for key, items in menu_sections.items()]
        
        context = {
            'menu_sections': menu_sections_list
        }
        return render(request, 'nonvegmenu.html', context)

#manage food
class AddFood(LoginRequiredMixin, View):
    login_url = '/'
    
    def get(self, request):
        nv_form = NVForm()
        veg_form = VegForm()
        context = {'nv_form': nv_form, 'veg_form': veg_form}
        return render(request, 'addfood.html', context)
    
    def post(self, request):
        if 'nvsubmit' in request.POST: 
            nv_form = NVForm(request.POST, request.FILES)  
            if nv_form.is_valid():
                nv_form.save()  
                return redirect('/menu/add/') 
            else:
                return render(request, 'addfood.html', {'nv_form': nv_form, 'veg_form': VegForm()})
        elif 'vegsubmit' in request.POST:
            veg_form = VegForm(request.POST, request.FILES)  
            if veg_form.is_valid():
                veg_form.save()  
                return redirect('/menu/add/') 
            else:
                return render(request, 'addfood.html', {'veg_form': veg_form, 'nv_form': NVForm()})
        return render(request, 'addfood.html', {'nv_form': NVForm(), 'veg_form': VegForm()})
      
@login_required(login_url='/')
def food_table(request):
    context = {
        'vegi' : VegMenu.objects.all(),
        'nonvegi' : NonVegMenu.objects.all(),
    }
    return render(request, 'foodtable.html',context)

@login_required(login_url='/')
def food_vegtable_update(request,id):
    up = get_object_or_404(VegMenu, id=id)
    if request.method == 'POST':
        vegform = VegForm(request.POST,instance=up)
        if vegform.is_valid():
            vegform.save()
            return redirect('/menu/add-food/')
    else:
        vegform = VegForm(instance=up)
    context = {
        'vegform': vegform
    }
    return render(request,'addfood.html',context)

@login_required(login_url='/')
def food_vegtable_delete(request, id):
    up = get_object_or_404(VegMenu, id=id)
    up.delete()
    return redirect('/menu/add-food/')

@login_required(login_url='/')
def food_nvtable_update(request,id):
    up = get_object_or_404(NonVegMenu, id=id)
    if request.method == "POST":
        nvform = NVForm(request.POST,instance = up)
        if nvform.is_valid():
            nvform.save()
            return redirect('/menu/add-food/')
    else:
        nvform = NVForm(instance=up)
            
    context = {
            'nvoform': nvform
        }
    return render (request,'addfood.html',context)

@login_required(login_url='/')
def food_nvtable_delete(request,id):
    up = get_object_or_404(NonVegMenu, id=id)
    up.delete()
    return redirect('/menu/add-food/')


#cart session
class RemoveFromCart(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request, item_id=None):
        cart = request.session.get('cart', {})
        action = request.POST.get('action')

        if item_id and str(item_id) in cart:
            if action == "decrement":
                if cart[str(item_id)]['quantity'] > 1:
                    cart[str(item_id)]['quantity'] -= 1
                    cart[str(item_id)]['total'] = cart[str(item_id)]['quantity'] * cart[str(item_id)]['price']
                else:
                    del cart[str(item_id)]
            elif action == "remove_all":
                del cart[str(item_id)]
        
        # Update the session cart
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('/menu/cart/')


class AddToCart(SuccessMessageMixin, LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request, idv=None, idnv=None):
        cart = request.session.get('cart', {})

        # Determine the item type based on the provided IDs
        if idnv:  # If the non-veg ID is provided
            try:
                item = NonVegMenu.objects.get(id=idnv)
                item_type = 'nonveg'
                item_id = idnv
            except NonVegMenu.DoesNotExist:
                return redirect('/menu/nvmenu/')  # Handle the case where the item doesn't exist
        elif idv:  # If the veg ID is provided
            try:
                item = VegMenu.objects.get(id=idv)
                item_type = 'veg'
                item_id = idv
            except VegMenu.DoesNotExist:
                return redirect('/menu/vegmenu/')  # Handle the case where the item doesn't exist
        else:
            return redirect('/menu/home/')  # If no valid ID is provided

        # Add item to the cart
        if str(item_id) in cart:
            if cart[str(item_id)]['item_type'] == item_type:
                cart[str(item_id)]['quantity'] += 1
                cart[str(item_id)]['total'] = cart[str(item_id)]['quantity'] * cart[str(item_id)]['price']
            else:
                new_id = f"{item_type}_{item_id}"
                cart[new_id] = {
                    'name': item.name,
                    'price': float(item.price),
                    'quantity': 1,
                    'total': float(item.price),
                    'item_type': item_type,
                }
        else:
            cart[str(item_id)] = {
                'name': item.name,
                'price': float(item.price),
                'quantity': 1,
                'total': float(item.price),
                'item_type': item_type,
            }

        # Save the updated cart back to the session
        request.session['cart'] = cart

        # Display an alert message
        item_name = cart[str(item_id)]['name']
        messages.success(request, f"{item_name} has been added to the cart. You can go to your cart now!")

        # Redirect back to the referring page
        next_url = request.POST.get('next', '/menu/home/')  # Fallback to home if 'next' is not provided
        return redirect(next_url)


class Cart(LoginRequiredMixin,View):
    login_url = '/'
    def get(self, request):
        cart = request.session.get('cart', {})
        #print("Cart retrieved from session:", cart) 
        total_price = sum(item['total'] for item in cart.values())

        context = {
            'cart': cart,
            'total_price': total_price
        }
        return render(request, 'cart.html', context)



#order process
@login_required(login_url='/')
def checkout(request):
    cart = request.session.get('cart', {})
    sub_total = sum(item['total'] for item in cart.values())
    handling_fee = 30
    gst = sub_total * 0.06
    total_price = sub_total + gst + handling_fee
    
    user = request.user
    addresses = Address.objects.filter(user=user)  # Current user's addresses only
    
    if request.method == "POST":
        selected_address_id = request.POST.get("selected_address")
        selected_address = Address.objects.get(id=selected_address_id, user=user)
        print(selected_address)
        # Save selected address to session or process further
        request.session['selected_address'] = selected_address_id
        return redirect('payment')  # Redirect to the payment page

    context = {
        'sub_total': sub_total,
        'total_price': total_price,
        'handling_fee': handling_fee,
        'gst': gst,
        'addresses': addresses
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='/')
def payment(request):
    # Retrieve selected address from session
   
 
    # Get the cart from the session
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('/')  # Redirect if cart is empty

    # Calculate totals
    sub_total = sum(item['total'] for item in cart.values())
    handling_fee = 30
    gst = sub_total * 0.12
    total_price = sub_total + gst + handling_fee

    # Provide the context for rendering the payment page
    context = {
        'total_price': total_price,
        'cart_items': cart.values(),  # Pass the cart items to the context
    }
    return render(request, 'paymentpage.html', context)


@login_required(login_url='/')
def order_placed(request):
    if request.method == 'POST':
        # Retrieve the selected address from session
        address_id = request.session.get('selected_address')
        if not address_id:
            return redirect('checkout')  # If no address is selected, redirect to checkout

        try:
            selected_address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return redirect('checkout')  # If invalid address, redirect to checkout

        # Combine address details into a single string
        full_address = f"{selected_address.street}, {selected_address.address_line_1}, {selected_address.address_line_2}, {selected_address.state}"

        # Get the cart from the session
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('/')  # Redirect home if cart is empty

        # Calculate totals
        sub_total = sum(item['total'] for item in cart.values())
        handling_fee = 30
        gst = sub_total * 0.12
        total_price = sub_total + gst + handling_fee

        # Save the order
        order = Order.objects.create(
            user=request.user,
            sub_total=sub_total,
            handling_fee=handling_fee,
            gst=gst,
            total_price=total_price,
            address=full_address  # Save the formatted address
        )

        # Save cart items related to the order
        for item in cart.values():
            CartItem.objects.create(
                order=order,
                name=item['name'],
                quantity=item['quantity']
            )

        # Clear the cart after saving
        del request.session['cart']
        del request.session['selected_address']  # Clear the selected address
        request.session.modified = True

        return render(request, 'order_placed.html', {'order': order})



@login_required(login_url='/')
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).prefetch_related('cart_items')

    context = {
        'orders': orders,
    }

    return render(request, 'order_details.html', context)


@login_required(login_url='/')
def order_delete(request, order_id):
    # Get the order object or return a 404 if not found
    order = get_object_or_404(Order, id=order_id)

    if request.user:
        # Delete the order
        order.delete()
       
        # Redirect to the order history page after deletion
        return redirect('order_history')

    
#search
def search_menu(request):
    query = request.GET.get('q', '')  # Get the search query
    veg_results = VegMenu.objects.filter(name__icontains=query)  # Search in VegMenu
    nonveg_results = NonVegMenu.objects.filter(name__icontains=query)  # Search in NonVegMenu
    
    context = {
        'query': query,
        'veg_results': veg_results,
        'nonveg_results': nonveg_results,
    }
    return render(request, 'search_results.html', context)
 
 
 
#address
def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Ensure the user associated with the address is the current logged-in user
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout')
    else:
        form = AddressForm()

    context = {
        'form': form,
    }
    return render(request, 'address_create.html', context)


def show_address(request):
    if request.user.is_superuser:
        # If the user is a superuser, show all users who have addresses
        users = User.objects.filter(address__isnull=False).distinct()
        addresses = Address.objects.filter(user__in=users)
    else:
        # For regular users, only show their own addresses
        users = [request.user]
        addresses = Address.objects.filter(user=request.user)

    context = {
        'users': users,
        'addresses': addresses,
    }
    return render(request, 'address_show.html', context)



@login_required
def address_update(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_show')
    else:
        form = AddressForm(instance=address)

    context = {
        'form': form,
        'address': address,
    }
    return render(request, 'address_update.html', context)



@login_required
def address_delete(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    if request.method == 'POST':
        address.delete()
        return redirect('address_show')  # Redirect to the address listing page after deletion

    context = {
        'address': address,
    }
    return render(request, 'address_delete.html', context)

