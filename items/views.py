from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import ListView

import base64
from pathlib import Path
from PIL import Image
import cloudinary
from cloudinary.uploader import upload
from .models import Item, ItemType
from .forms import (
    ItemTypeForm, ItemTypeEditForm, ItemTypeCreateForm, ItemTypeFullForm,
    ItemForm, ItemCreateForm, ItemStatusForm, )


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


@method_decorator(login_required, name='dispatch')
class ItemTypeList(ListView):
    """
    Class ListView to display the item types into a table.
    """
    paginate_by = 10
    model = ItemType
    template_name = 'items/item_type_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemTypeList, self).get_context_data(**kwargs)
        print(context)
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
        # selected_type = get_object_or_404(
        #     ItemType,
        #     pk=request.POST['edit-item-item_type'])
        # item_new.type = selected_type
        # item_new.item_type = selected_type
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
        item_status_form = ItemStatusForm(
            prefix="status", item_id=item.id)

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
        'item_status': item.this_template_status(),
        'template_status': item.template_status(),
        'status_css': item.item_css_status(),
        'account_type': account_type,
        'all_types': item_type_list,
        'item_type_form': item_type_form,
        'item_form': item_form,
        'item_type_edit_form': item_type_edit_form,
        'item_status_form': item_status_form,
    }

    return render(request, template, context)


@login_required
def item_type_view(request, type_id):
    """
    View to display the properties of an individual item type
    """
    print(type_id)
    print(request)
    item_type = get_object_or_404(ItemType, pk=type_id)

    print(item_type)
    # account_type = request.user.profile.get_account_type()

    # When form is submitted, note to ignore the ItemType form, they are
    # disabled in the form and they are display only, carrying the values
    # from it's own model for display.
    if request.method == "POST":

        # Work with a duplicate of the original instance, just in case
        item_type_new = item_type
        item_type_form = ItemTypeFullForm(request.POST)
        # Only need to search for the one prefix, because someone without
        # "edit" should not be able to change the details and they are
        # display only
        # selected_type = get_object_or_404(
        #     ItemType,
        #     pk=request.POST['edit-item-item_type'])
        # item_new.type = selected_type
        # item_new.item_type = selected_type

        # try:
        #     item_new.full_clean()
        # except ValidationError as e:
        #     messages.error(
        #         request, (
        #             e,
        #             'Item data is not valid.'
        #             'Please check the validation prompts.'
        #         )
        #     )
        #     pass

        # item_new.save()

        # Display a message to the user to show it has worked
        messages.success(
            request,
            'Item successfully updated'
        )

        return redirect('item_type_view', type_id=item_type_new.id)

    else:

        item_type_form = ItemTypeFullForm(instance=item_type)
        # return redirect('item_type_view', type_id=item_type.id)
        # The query is a GET. So data/context/template needs to
        # sent to the form to load.

        # queryset = ItemType.objects.all()
        # item_type_list = list(queryset)

        # item_type_form = ItemTypeFullForm(instance=item_type)

    # Set template and context
    # print("Hello")

    template = 'items/item_type.html'
    context = {
        'item_type_name': item_type.name,
        'item_type_form': item_type_form,
        'item_type_image': item_type.image
    }

    return render(request, template, context)


@login_required
def item_type_create(request):

    account_type = request.user.profile.get_account_type()
    all_categories = (
        ItemType.objects.values('category').distinct('category'))
    # item_type_list = list(item_type_queryset)
    # 'all_types': item_type_list,
    # print(previous_categories)
    # This will determine if they have navigated by the url directly.
    # If they are a customer, it will bump that to the main menu, all
    # other accounts (Staff,HR,Administrator) are permitted to do this.
    if account_type == 'Customer':
        messages.error(
            request, 'Permission Denied : A customer cannot add items.')
        return redirect('menu')
    else:
        if request.method == "POST":
            upload_result = None
            form = ItemTypeCreateForm(request.POST)
            # This allows the use of a text field in the category section.
            # Giving the ability now to select a previously used category or
            # to create a new one.print("FORM")

            if form.is_valid():
                form.clean_category()
                print("HERE1")
                image_name = form.data['image-input-name']
                # Check the file does not already exist
                if Path(f"{settings.MEDIA_ROOT}/{image_name}").exists():
                    pass
                    # Check that the user has not submitted a "No Image"
                elif form.data['image-input-name'] == ("No Image"):
                    # Although no image exists, another is not required
                    image_name = "/static/images/default.webp"
                else:
                    
                    # If the file does not exist, then create one
                    # take the file from the "image-button"
                    if 'image-button' in request.FILES:
                        
                        try:
                            print("In the files")
                            upload_result = upload(
                                request.FILES['image-button'],
                                use_filename=True)
                            print(upload_result)

                        except IOError:
                            print("HERE4")
                            image_name = "/static/images/default.webp"

                            messages.error(
                                request, (
                                    'An error occurred while trying'
                                    ' to open the image.'
                                    ' Default image will be used'
                                )
                            )
                        print("HERE4")
                        pass
                    else:
                        # If no image uploaded /static/images/default.webp
                        print("HERE5")
                        image_name = "settings.DEFAULT_NO_IMAGE"
                        new_item_type = form

                try:
                    print("HERE6")
                    form.full_clean()
                    print(form.full_clean())

                except ValidationError as e:
                    print("HERE7")
                    messages.error(
                        request, (
                            e,
                            'Item type data is not valid.'
                            'Please check the validation prompts.'
                        )
                    )
                print("HERE8")
                new_item_type = form.save(commit=False)
                new_item_type.image = upload_result["secure_url"]
                new_item_type.save()
                new_type_id = new_item_type.id
                messages.success(
                    request, 'This type has been newly created')
                return redirect('item_type_view', new_type_id)
            else:
                print("HERE9")
                messages.error(
                    request,
                    (
                        'Could not add the item type.'
                        'Check the form for validation.'
                    )
                )
        else:
            form = ItemTypeCreateForm()

        template = 'items/item_type_create.html'
        context = {
            'all_categories': all_categories,
            'item_type_create_form': form,
            'item_type_image': static('images/default.webp')
        }
    return render(request, template, context)


@login_required
def item_type_update_inline(request, item_id, type_id):
    """
    View to display the properties of an individual item type within an item.
    It only responds to POST so there is no requirement for a
    GET return response.
    It needs to determine :
    - If it is a new item type
    Or
    - If it is an old item type that is the same
    Or
    - If it is an old item type that has been modified
    """
    item = get_object_or_404(Item, pk=item_id)
    account_type = request.user.profile.get_account_type()
    upload_result = None
    # When form is submitted.
    if request.method == "POST":
        if account_type == 'Administrator':

            # Work with a duplicate of the original instance, just in case
            submit_type_form = ItemTypeForm(request.POST, request.FILES)
            submit_type_name = submit_type_form.data['edit-type-name']
            submit_type_category = submit_type_form.data['edit-type-category']
            print("----- FORM DATA ----")
            print(submit_type_form.data)
            new_or_old_type = "new"

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

            # item_type_check = ItemType.objects.filter(
            #     Q(name__iexact=submit_type_name) &
            #     Q(category__iexact=submit_type_category))

            item_type_check = ItemType.objects.get(
                Q(name__iexact=submit_type_name) &
                Q(category__iexact=submit_type_category))

            previous_image_exists = False
            # image_name = submit_type_form.data['image-input-name']
            # Check the file does not already exist
            if submit_type_form.data['image-input-name'] == ("No Image"):
                # Although no image exists, another is not required
                previous_image_exists = False
                image_name = settings.DEFAULT_NO_IMAGE
            else:
                # If the file does not exist, then create one
                previous_image_exists = True
                # If there is a file with image-button as a key


            if item_type_check:
                # If entry found, then this is an update of a previous object
                # Use the found item for data update and save
                new_or_old_type = "old"

                # Get a copy of the ItemType object
                update_type = get_object_or_404(ItemType, pk=type_id)
                # Amend the ItemType for the new values
                update_type.name = submit_type_name
                # sku is unique and should be kept
                update_type.sku = submit_type_form.data['edit-type-sku']
                update_type.category = (
                    submit_type_form.data['edit-type-category'])
                update_type.cost_initial = (
                    submit_type_form.data['edit-type-cost_initial'])
                update_type.cost_week = (
                    submit_type_form.data['edit-type-cost_week'])
                # If true, as obtained by previous function.
                if previous_image_exists is True:

                    if 'image-button' in request.FILES:
                        try:
                            print("In the files")
                            upload_result = upload(
                                request.FILES['image-button'],
                                use_filename=True)
                            print(upload_result)

                        except IOError:
                            image_name = settings.DEFAULT_NO_IMAGE

                            messages.error(
                                request, (
                                    'An error occurred while trying'
                                    ' to open the image.'
                                    ' Default image will be used'
                                )
                            )
                            pass
                        update_type.image = upload_result["secure_url"]
                    # Use the original image value
                    else:
                        update_type.image = update_type.image
                else:
                    # Use the newly created image value
                    if 'image-button' in request.FILES:
                        try:
                            print("In the files")
                            upload_result = upload(
                                request.FILES['image-button'],
                                use_filename=True)
                            print(upload_result)

                        except IOError:
                            image_name = settings.DEFAULT_NO_IMAGE

                            messages.error(
                                request, (
                                    'An error occurred while trying'
                                    ' to open the image.'
                                    ' Default image will be used'
                                )
                            )
                            pass
                        update_type.image = upload_result["secure_url"]
                    else:
                        update_type.image = settings.DEFAULT_NO_IMAGE

                # Until implementation, do not update the meta_tags field
                update_type.meta_tags = update_type.meta_tags
                print("----- UPDATE DATA ----")
                print(update_type)
                print("old save")
                update_type.save()

                # Then needs to set this type to the item (this allows for
                # updated to different type, or updated original type)

                # Auto increment key means that the id
                # can be gained after save())
                item.item_type = get_object_or_404(
                    ItemType, pk=update_type.id)

                # Then save the item with updated type
                item.save()

            else:

                new_or_old_type = "new"
                # If no ItemType found, then a new ItemType object must be made
                new_item_type = ItemType(
                    name=submit_type_form.data['edit-type-name'],
                    sku=submit_type_form.data['edit-type-sku'],
                    category=submit_type_form.data['edit-type-category'],
                    cost_initial=submit_type_form.data[
                        'edit-type-cost_initial'],
                    cost_week=submit_type_form.data[
                        'edit-type-cost_week'],
                    image=image_name,
                    meta_tags=None
                )
                print("----- NEW DATA ----")
                print(new_item_type)
                print("new save")
                # Save the new object
                new_item_type.save()

                # Then needs to set this type to the item
                # item = get_object_or_404(Item, pk=item_id)

                # Auto increment key means that the id
                # can be gained after save())
                item.item_type = get_object_or_404(
                    ItemType, pk=new_item_type.id)

                # Then save the item with updated type
                item.save()

        else:
            if account_type == "Customer":
                messages.error(
                    request,
                    "Permission Denied: A customer cannot edit an item")
                return redirect('menu')
            else:
                # This person staff but not an administrator
                # Display a message to the user to tell them no access
                messages.error(
                    request,
                    'Permission Denied: Unauthorised to make these changes'
                )
                return redirect('item_view', item_id=item_id)

        # Display a message to the user to show it has worked
        if new_or_old_type == "new":
            messages.success(
                request,
                'Item Type created'
            )
        else:
            messages.success(
                request,
                'Item Type updated'
            )

        return redirect('item_view', item_id=item_id)

    else:
        # The query is a GET. So data/context/template needs to
        # sent to the form to load.
        pass


@login_required
def item_create(request):

    account_type = request.user.profile.get_account_type()

    item_type_queryset = ItemType.objects.all()
    item_type_list = list(item_type_queryset)

    # This will determine if they have navigated by the url directly.
    # If they are a customer, it will bump that to the main menu, all
    # other accounts (Staff,HR,Administrator) are permitted to do this.
    if account_type == 'Customer':
        messages.error(
            request, 'Permission Denied : A customer cannot add items.')
        return redirect('menu')
    else:
        if request.method == 'POST':
            form = ItemCreateForm(request.POST)
            if form.is_valid():
                # Only one extra validation, there should not be an instance
                # where the serial and type already exist together

                new_item = form.save(commit=False)

                try:
                    item_check = Item.objects.get(
                        Q(item_type__exact=new_item.item_type) &
                        Q(item_serial=new_item.item_serial))
                    print(item_check)
                    print(item_check.id)

                    check_type_id = item_check.id
                    check_serial = item_check.item_serial
                    url_construct = (
                        f'<span>'
                        f'<a href="/items/{check_type_id}">{check_serial}</a>'
                        f' Already exists.</span>'
                    )

                    messages.error(
                        request,
                        mark_safe(url_construct)
                    )

                except ObjectDoesNotExist:

                    new_item = form.save()
                    new_item_id = new_item.id
                    messages.success(
                        request, 'This Item has been newly created')
                    return redirect('item_view', new_item_id)
            else:
                messages.error(
                    request,
                    (
                        'Could not add the item.'
                        'Check the form for validation.'
                    )
                )
        else:
            form = ItemCreateForm()

        template = 'items/item_create.html'
        context = {
            'all_types': item_type_list,
            'item_create_form': form,
        }

        return render(request, template, context)


@login_required
def item_status_edit(request, item_id):
    print("-----------------")
    print(request.POST)
    print(item_id)
    print("-----------------")
    account_type = request.user.profile.get_account_type()
    if account_type == 'Customer':
        messages.error(
            request,
            "Permission Denied : A customer cannot edit an item's status.")
        return redirect('menu')
    else:
        if request.method == 'POST':
            item = get_object_or_404(Item, pk=item_id)
            form = ItemStatusForm(
                request.POST, item_id=item_id, prefix="status")
            item.status = form.data['status-status']
            item.save()

            messages.success(
                request, 'The status has been updated')
            return redirect('item_view', item_id)
        else:
            # form = ItemStatusForm(item_id=item_id, prefix="status-")
            pass
            messages.error(
                    request,
                    (
                        'Could not update the status.'
                        'Contact an IT Administrator.'
                    )
                )
