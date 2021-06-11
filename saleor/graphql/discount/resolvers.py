from ...core.tracing import traced_resolver
from ...discount import models
from ..channel import ChannelContext, ChannelQsContext
from ..utils.filters import filter_by_query_param

VOUCHER_SEARCH_FIELDS = ("name", "code")
SALE_SEARCH_FIELDS = ("name", "value", "type")


def resolve_voucher(id, channel):
    sale = models.Voucher.objects.filter(id=id).first()
    return ChannelContext(node=sale, channel_slug=channel) if sale else None


@traced_resolver
def resolve_vouchers(info, query, channel_slug, **_kwargs) -> ChannelQsContext:
    qs = models.Voucher.objects.all()
    qs = filter_by_query_param(qs, query, VOUCHER_SEARCH_FIELDS)
    if channel_slug:
        qs = qs.filter(channel_listings__channel__slug=channel_slug)
    return ChannelQsContext(qs=qs, channel_slug=channel_slug)


def resolve_sale(id, channel):
    sale = models.Sale.objects.filter(id=id).first()
    return ChannelContext(node=sale, channel_slug=channel) if sale else None


@traced_resolver
def resolve_sales(info, query, channel_slug, **_kwargs) -> ChannelQsContext:
    qs = models.Sale.objects.all()
    qs = filter_by_query_param(qs, query, SALE_SEARCH_FIELDS)
    if channel_slug:
        qs = qs.filter(channel_listings__channel__slug=channel_slug)
    return ChannelQsContext(qs=qs, channel_slug=channel_slug)
