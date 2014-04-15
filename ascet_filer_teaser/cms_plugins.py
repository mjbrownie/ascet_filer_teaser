from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
import models
from django.conf import settings

from django.contrib import admin

try:
    from settings import TEASER_PLUGIN_TEMPLATES
except:
    TEASER_PLUGIN_TEMPLATES = (
            ('intro_widget.html', 'Slider List'),
            )


class FilerTeaserItemInline(admin.TabularInline):

    model = models.FilerTeaserItem

class FilerTeaserListPlugin(CMSPluginBase):

    model = models.FilerTeaserList
    module = 'Filer'
    name = _("FilerTeaserList")
    render_template = TEASER_PLUGIN_TEMPLATES[0][0]
    filter_horizontal = ('filer_teasers',)

    inlines = [FilerTeaserItemInline,]

    def render(self, context, instance, placeholder):
        if instance and instance.template:
            self.render_template = instance.template
        context.update({
            'object':instance, 
            'placeholder':placeholder,
            'teasers':instance.filer_teasers.all()
        })
        return context

plugin_pool.register_plugin(FilerTeaserListPlugin)
