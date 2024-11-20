from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect  # , reverse
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from PIL import Image

from .models import Item, ItemType
from .forms import ItemTypeForm, ItemTypeEditForm, ItemForm


@method_decorator(login_required, name='dispatch')
class ItemList(ListView):
    """
    Class ListView to display the items into a table.
    """
    paginate_by = 10
    model = Item
    template_name = 'items/item_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        return context


@login_required
def item_view(request, item_id):
    """
    View to display the properties of an individual item
    """

    item = get_object_or_404(Item, pk=item_id)
    account_type = request.user.profile.get_account_type()

    # When form is submitted, note to ignore the ItemType form, they are
    # disabled in the form and they are display only, carrying the values
    # from it's own model for display.
    if request.method == "POST":

        # Work with a duplicate of the original instance, just in case
        item_new = item
        # Only need to search for the one prefix, because someone without
        # "edit" should not be able to change the details and they are
        # display only
        selected_type = get_object_or_404(
            ItemType,
            pk=request.POST['edit-item-item_type'])
        item_new.type = selected_type
        item_new.item_type = selected_type
        item_new.item_serial = request.POST['edit-item-item_serial']

        try:
            item_new.full_clean()
        except ValidationError as e:
            messages.error(
                request, (
                    e,
                    'Item data is not valid.'
                    'Please check the validation prompts.'
                )
            )
            pass

        item_new.save()

        # Display a message to the user to show it has worked
        messages.success(
            request,
            'Item successfully updated'
        )

        return redirect('item_view', item_id=item_new.id)

    else:
        # The query is a GET. So data/context/template needs to
        # sent to the form to load.
        if account_type == "Administrator":
            extra_prefix = "edit-"

        queryset = ItemType.objects.all()
        item_type_list = list(queryset)

        # testing
        # for x in item_type_list:
        #     print(x.sku)

        item_form = ItemForm(
            account_type=account_type,
            instance=item, prefix=f"{extra_prefix}item")
        item_type_form = ItemTypeForm(
            account_type=account_type,
            instance=item.item_type, prefix="type")
        item_type_edit_form = ItemTypeEditForm(
            account_type=account_type, item_id=item.id,
            instance=item.item_type, prefix="edit-type")

    # Set template and context
    template = 'items/item.html'
    context = {
        # 'current_user': request.user,
        'item_id': item.id,
        'item_type_category': item.item_type.category,
        'item_serial': item.item_serial,
        'item_type_sku': item.item_type.sku,
        'item_income': item.income,
        'item_type_image': item.item_type.image,
        'item_type_name': item.item_type.name,
        'status_css': item.item_css_status(),
        'account_type': account_type,
        'all_types': item_type_list,
        'item_type_form': item_type_form,
        'item_form': item_form,
        'item_type_edit_form': item_type_edit_form,
    }

    return render(request, template, context)


@login_required
def item_type_update_inline(request, item_id, type_id):
    """

    View to display the properties of an individual item type within an item.
    It only responds to POST so there is no requirement for a GET return response.
    It needs to determine :
    - If it is a new item type
    Or
    - If it is an old item type that is the same
    Or
    - If it is an old item type that has been modified

    """
    # item = get_object_or_404(Item, pk=item_id)
    # item_type = get_object_or_404(ItemType, pk=type_id)
    account_type = request.user.profile.get_account_type()

    # When form is submitted.
    if request.method == "POST":
        if account_type == 'Administrator':
            # Work with a duplicate of the original instance, just in case

            submit_type_form = ItemTypeForm(request.POST, request.FILES)
            submit_type_name = submit_type_form.data['edit-type-name']
            submit_type_category = submit_type_form.data['edit-type-category']
            print("----- FORM DATA ------")
            print(submit_type_form.data)
            item_type_check = ItemType.objects.filter(
                Q(name__iexact=submit_type_name) &
                Q(category__iexact=submit_type_category))
            print("----- FIND DUPLICATE ------")
            print(item_type_check.values())
            # test
            # print(model_to_dict(item_type_check))
            if item_type_check.exists():

                update_type = get_object_or_404(ItemType, pk=type_id)
                # image_name = slugify(submit_type_name)+'.webp'
                image_name = "test2.webp"
                print("----- UPDATE TYPE 1 ------")
                print(vars(update_type))
                # If entry found, then this is an update of a previous object
                # Use the found item for data update and save
                print("Found")
                # submit_type_image = None
                # name,sku,category,cost_initial,cost_week,image,meta_tags
                update_type.name = submit_type_name
                update_type.sku = submit_type_form.data['edit-type-sku']
                update_type.category = submit_type_category
                update_type.cost_initial = submit_type_form.data['edit-type-cost_initial']
                update_type.cost_week = submit_type_form.data['edit-type-cost_week']
                # Until implementation, do not update the meta_tags field
                update_type.meta_tags = update_type.meta_tags
                print(request.FILES)
                if 'edit-image-button' in request.FILES:
                    print("---- File Found ----- ")
                    try:
                        with Image.open(request.FILES['edit-image-button']) as img:
                            print("IMG")
                            print(img)
                            img.convert('RGB')
                            img.name = "test2.webp"
                            img_path = f"{settings.MEDIA_ROOT}/{image_name}"
                            print("Name")
                            print(img.name)
                            print("Path")
                            print(img_path)
                            img.save(img_path, 'webp')
                            # img

                    except IOError:
                        print("An error occurred while trying to open the image.")
                    # submit_type_image = Image.open(request.FILES)
                    # submit_type_image = Image.open(request.FILES['edit-image-button'])
                    # submit_type_image.save(image_name, 'webp')
                    # image_field = Image.open()
                    # image_field.convert('RGB')
                    # image_name = slugify(submit_type_name)+'.webp'
                    # image_name = "test.webp"
                    print("---- INIT FILE GET ----")
                    update_type.image = image_name

                    # print(submit_type_image)
                    # submit_type_image = submit_type_image.convert('RGB')
                    # image_name = slugify(submit_type_name)+'.webp'
                    # submit_type_image.save(image_name, 'webp')
                    # print("---- AFTER SAVE ----")
                    # print(submit_type_image)

                    # update_type.image = request.FILES['edit-image-button']
                else:
                    # pass
                    update_type.image = update_type.image

                print("----- UPDATE TYPE 2 ------")
                print(vars(update_type))
                # print("------SHOW-------")
                # print(submit_type_image.show())
                # print("-----NO SHOW------")
                update_type.save()
                # print(update_type.image.url)
                # print(submit_type_form.name)
                # print(item_type_check.name)
                # update_user.first_name = profile_form.data['first_name']
                # update_user.last_name = profile_form.data['last_name']
                # # Email is entered from the request.user, not the form post.
                # update_user.email = request.user.email
                # profile.address_line_1 = profile_form.data['address_line_1']
                # profile.address_line_2 = profile_form.data['address_line_2']
                # profile.address_line_3 = profile_form.data['address_line_3']
                # profile.town = profile_form.data['town']
                # profile.county = profile_form.data['county']
                # profile.country = profile_form.data['country']
                # profile.postcode = profile_form.data['postcode']
                # profile.phone_number = profile_form.data['phone_number']

            else:
                # If no entry found, this is a new object
                print("Not Found")

        # item_new.type = selected_type
        # item_new.item_type = selected_type
        # item_new.item_serial = request.POST['edit-item-item_serial']
        # item_type_form = ItemTypeForm(request.POST, request.FILES)
        # print(request.POST)
        # item_type_new.name = request.POST['edit-type-name']
        # item_type_new.sku = request.POST['edit-type-sku']
        # item_type_new.category = request.POST['edit-type-category']
        # item_type_new.cost_initial = request.POST['edit-type-cost_initial']
        # item_type_new.cost_week = request.POST['edit-type-cost_week']
        # [NICE] If time will include a meta tags field
        # item_type_new.meta_tags = item_type_new.meta_tags

        try:
            submit_type_form.full_clean()
        except ValidationError as e:
            messages.error(
                request, (
                    e,
                    'Item type data is not valid.'
                    'Please check the validation prompts.'
                )
            )
            pass
        
        # testing
        # print(submit_type_form.data)

        # item_type_new.save()
        print("----- UPDATE TYPE 2 ------")
        print(vars(update_type))
        # Display a message to the user to show it has worked
        messages.success(
            request,
            'Item Type updated. Reloaded Item page'
        )

        return redirect('item_view', item_id=item_id)

    else:
        # The query is a GET. So data/context/template needs to
        # sent to the form to load.
        # if account_type == "Administrator":
        #     extra_prefix = "edit-"

        # item_form = ItemForm(
        #     account_type=account_type,
        #     instance=item, prefix=f"{extra_prefix}item")
        # item_type_form = ItemTypeForm(
        #     account_type=account_type,
        #     instance=item.item_type, prefix="type")
        # item_type_edit_form = ItemTypeEditForm(
        #     account_type=account_type,
        #     instance=item.item_type, prefix="edit-type")
        print("GET FORM")
    # Set template and context
    # template = 'items/item.html'
    # context = {
    #     # 'current_user': request.user,
    #     'item_id': item.id,
    #     'item_serial': item.item_serial,
    #     'item_income': item.income,
    #     'item_image': item.item_type.image,
    #     'item_type_name': item.item_type.name,
    #     'image_border': item.item_css_status(),
    #     'account_type': account_type,
    #     'item_type_form': item_type_form,
    #     'item_form': item_form,
    #     'item_type_edit_form': item_type_edit_form,
    # }

    # return render(request, template, context)