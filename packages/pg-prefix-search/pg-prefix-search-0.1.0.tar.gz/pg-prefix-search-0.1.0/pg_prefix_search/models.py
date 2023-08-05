from django.db import models
from django.db.models.functions import Upper
from django.contrib.postgres.indexes import GinIndex, OpClass


class ImmutableUnaccent(models.Func):
    function = 'imm_unaccent'


def text_searchable_index_spec(field_name):
    """
    Specification of GIN index for a column that should be full-text searchable.
    This exact index format is important, the following contains benchmarks that prove it:
    https://gist.github.com/ssobczak/572fdda8ad7aef91abe968c5fcc755ff
    """
    return OpClass(Upper(ImmutableUnaccent(field_name)), 'gin_trgm_ops')


class SearchableModel(models.Model):
    name = models.CharField('Nazwa', max_length=1024)

    class Meta:
        abstract = True

        indexes = (
            GinIndex(text_searchable_index_spec('name'), name='searchable_model_name__gin'),
        )
