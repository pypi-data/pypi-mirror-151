from django.db.models import QuerySet, Q
from unidecode import unidecode

from pg_prefix_search.models import ImmutableUnaccent


def apply_search_by_name(queryset, field_name, query_text) -> QuerySet:
    """
    Builds a correct fill-text search query part:
    - allows searching by word beginnings ("rej kra gosp" -> "Sąd Rejonowy w Krakowie wydział Gospodarczy")
    - making sure that DB index is used
    - handling polish accent letters and upper/lower case
    """
    queryset = queryset.annotate(search_field_unaccented=ImmutableUnaccent(field_name))
    q = build_search_query_by_word_beginnings(query_text)
    return queryset.filter(q)


def build_search_query_by_word_beginnings(query_text) -> Q:
    """Builds a Q object that searches by word beginnings ("rej kra gosp" -> "Sąd Rejonowy w Krakowie wydział Gospodarczy")"""

    q = Q()
    if not query_text:
        return q

    unaccented_term = unidecode(query_text)

    for word in unaccented_term.split(' '):
        if word:
            q = q & (
                Q(search_field_unaccented__istartswith=word) |
                Q(search_field_unaccented__icontains=' '+word)
            )

    return q
