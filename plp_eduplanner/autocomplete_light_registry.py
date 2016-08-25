import autocomplete_light.shortcuts as al
from plp_eduplanner import models

#TODO permissions check
al.register(models.Competition,
            search_fields=['^title'],
            attrs={
                'data-autocomplete-minimum-characters': 1,
            },
            widget_attrs={
                'data-widget-maximum-values': 10,
                'class': 'modern-style',
            },
            )
