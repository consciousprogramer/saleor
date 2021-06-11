from ...core.tracing import traced_resolver
from ...menu import models
from ..channel import ChannelContext, ChannelQsContext
from ..core.utils import from_global_id_or_error
from ..core.validators import validate_one_of_args_is_in_query
from ..utils.filters import filter_by_query_param

MENU_SEARCH_FIELDS = ("name",)
MENU_ITEM_SEARCH_FIELDS = ("name",)


@traced_resolver
def resolve_menu(info, channel, menu_id=None, name=None, slug=None):
    validate_one_of_args_is_in_query("id", menu_id, "name", name, "slug", slug)
    menu = None
    if menu_id:
        _, id = from_global_id_or_error(menu_id)
        menu = models.Menu.objects.filter(id=id).first()
    if name:
        menu = models.Menu.objects.filter(name=name).first()
    if slug:
        menu = models.Menu.objects.filter(slug=slug).first()
    return ChannelContext(node=menu, channel_slug=channel) if menu else None


@traced_resolver
def resolve_menus(info, channel, query, **_kwargs):
    qs = filter_by_query_param(models.Menu.objects.all(), query, MENU_SEARCH_FIELDS)
    return ChannelQsContext(qs=qs, channel_slug=channel)


def resolve_menu_item(id, channel):
    menu_item = models.MenuItem.objects.filter(pk=id).first()
    return ChannelContext(node=menu_item, channel_slug=channel) if menu_item else None


@traced_resolver
def resolve_menu_items(info, query, **_kwargs):
    qs = models.MenuItem.objects.all()
    return filter_by_query_param(qs, query, MENU_ITEM_SEARCH_FIELDS)
