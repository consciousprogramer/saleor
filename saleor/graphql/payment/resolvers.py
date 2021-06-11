from ...core.tracing import traced_resolver
from ...payment import models
from ..utils.filters import filter_by_query_param

PAYMENT_SEARCH_FIELDS = ["id"]


def resolve_payment_by_id(id):
    return models.Payment.objects.filter(id=id).first()


@traced_resolver
def resolve_payments(info, query):
    queryset = models.Payment.objects.all().distinct()
    return filter_by_query_param(queryset, query, PAYMENT_SEARCH_FIELDS)
