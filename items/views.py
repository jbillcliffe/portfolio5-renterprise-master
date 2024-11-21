from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import ListView

from pathlib import Path
from PIL import Image

from .models import Item, ItemType
from .forms import (
    ItemTypeForm, ItemTypeEditForm, ItemForm, ItemCreateForm)


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

            item_type_check = ItemType.objects.filter(
                Q(name__iexact=submit_type_name) &
                Q(category__iexact=submit_type_category))

            item_type_check = ItemType.objects.get(
                Q(name__iexact=submit_type_name) &
                Q(category__iexact=submit_type_category))

            image_name = submit_type_form.data['image-input-name']
            previous_image_exists = False

            # Check the file does not already exist
            if Path(f"{settings.MEDIA_ROOT}/{image_name}").exists():
                # If it exists, another one should not be created
                previous_image_exists = True
            # Check that the user has not submitted a "No Image"
            elif submit_type_form.data['image-input-name'] == ("No Image"):
                # Although no image exists, another is not required
                previous_image_exists = False
                image_name = settings.DEFAULT_NO_IMAGE
            else:
                # If the file does not exist, then create one
                previous_image_exists = False
                # If there is a file with edit-image-button as a key
                if 'edit-image-button' in request.FILES:
                    image_name = slugify(submit_type_name) + ".webp"
                    try:
                        print("In the files")
                        with (
                            Image.open(
                                request.FILES['edit-image-button']) as img):
                            img.convert('RGB')
                            # Create the image name to use
                            img.name = image_name
                            img_path = f"{settings.MEDIA_ROOT}/{image_name}"
                            img.save(img_path, 'webp')

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
                else:
                    # If no image uploaded /static/images/default.webp
                    image_name = settings.DEFAULT_NO_IMAGE

            if item_type_check.exists():
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
                    # Use the original image value
                    update_type.image = update_type.image
                else:
                    # Use the newly created image value
                    update_type.image = image_name

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
            # This person is not an administrator
            # Display a message to the user to tell them no access
            messages.error(
                request,
                'Unauthorised to make these changes'
            )

            return redirect('item_view', item_id=item_id)

        # Display a message to the user to show it has worked
        if new_or_old_type == "new":
            messages.success(
                request,
                'Item Type created. Reloaded Item page'
            )
        else:
            messages.success(
                request,
                'Item Type updated. Reloaded Item page'
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
            request, 'Permission denied : Customer cannot add items.')
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
