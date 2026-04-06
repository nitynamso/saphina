from django.db import models
from wagtail.models import Page, PreviewableMixin
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

# Bloques atómicos importados de tu archivo externo blocks.py
from .blocks import (HeadingBlock, ButtonBlock, 
                     BaseContentBlock, 
                     ColumnLayoutBlock,
                     AboutUsBlock,
                     MoreThanSupplierBlock,
                     CategoriesBlock,
                     BrandsCarouselBlock,
                     MissionBlock,
                     ValuesBlock,
                     WhyChooseShapinaBlock,
                     CommunityBannerBlock,
                     FAQSectionBlock,
                     SplitHeroBlock,
                     WhyChooseUsBlock,
                     CategoriesSectionBlock,
                     ContactSectionOscuroBlock,
                     ContactSectionClaroBlock,
                     VideoLandingBlock)

# ==========================================
# 1. IDENTIDAD GLOBAL Y CONFIGURACIÓN
# ==========================================

@register_snippet
class GlobalHeader(PreviewableMixin, models.Model):
    """
    Control central de la cabecera: Logo y Banner Superior.
    Afecta a todo el sitio simultáneamente.
    """
    title = models.CharField(max_length=255, default="Configuración de Cabecera")
    
    # --- LOGO ---
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo Principal"
    )
    logo_width = models.IntegerField(
        default=100, 
        verbose_name="Ancho del Logo (px)",
        help_text="Ajusta el tamaño del logo en la cabecera"
    )

    # --- TOP BAR (BANNER) ---
    address = models.CharField(max_length=255, default="13463 N W 19th Lane, Miami, FL 33182", verbose_name="Dirección")
    phone = models.CharField(max_length=50, default="+1 (786) 847-5568", verbose_name="Teléfono")
    
    # --- ESTILOS ---
    bg_color = models.CharField(max_length=7, default="#FAD02C", verbose_name="Color Fondo Banner (Hex)")
    text_color = models.CharField(max_length=7, default="#1a1a1a", verbose_name="Color Texto Banner (Hex)")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('logo_width'),
        ], heading="Branding / Logo"),
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone'),
        ], heading="Información del Banner Superior"),
        MultiFieldPanel([
            FieldPanel('bg_color'),
            FieldPanel('text_color'),
        ], heading="Estilos del Banner"),
    ]

    def __str__(self):
        return self.title

    def get_preview_template(self, request, mode_name):
        return "includes/header_preview.html"

    def get_preview_context(self, request, mode_name):
        return {"header": self}


@register_setting
class SiteSettings(BaseSiteSetting):
    """Configuraciones de redes sociales."""
    facebook = models.URLField(blank=True, help_text="URL de Facebook")
    instagram = models.URLField(blank=True, help_text="URL de Instagram")
    web3forms_key = models.CharField(
        max_length=100, 
        verbose_name="Llave de Web3Forms",
        help_text="Pega aquí la Access Key. Esto activará todos los formularios de contacto de la página web.",
        default="Sin Llave",
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('web3forms_key')
        ], heading="Configuracion General"),
    ]
    


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=100)
    icon_url = models.URLField(blank=True, verbose_name="URL del Icono (SVG)")
    icon = models.ForeignKey(
        'wagtailimages.Image', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='+'
    )
    url = models.URLField(blank=True)

    panels = [FieldPanel('name'), FieldPanel('icon_url'), FieldPanel('icon'), FieldPanel('url')]
    def __str__(self): return self.name


@register_snippet
class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField(blank=True)
    logo = models.ForeignKey(
        'wagtailimages.Image', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='+'
    )

    panels = [FieldPanel('name'), FieldPanel('logo_url'), FieldPanel('logo')]
    def __str__(self): return self.name

# ==========================================
# 2. DEFINICIÓN DE BLOQUES (STRUCTBLOCKS)
# ==========================================

class HeroSlideBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    button_text = blocks.CharBlock(required=False)
    button_link = blocks.CharBlock(required=False)

    class Meta:
        icon = 'image'
        label = 'Slide'

class SliderBlock(blocks.StructBlock):
    logo = ImageChooserBlock(required=False, label="Logo Flotante Opcional")
    logo_position = blocks.ChoiceBlock(choices=[
        ('top-6 left-6', 'Top Izquierda'),
        ('top-6 right-6', 'Top Derecha'),
        ('bottom-20 left-6', 'Bottom Izquierda'),
        ('bottom-20 right-6', 'Bottom Derecha'),
        ('top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2', 'Centro Total'),
    ], default='top-6 left-6')
    logo_width = blocks.ChoiceBlock(choices=[
        ('w-24', 'Pequeño'), ('w-32', 'Normal'), ('w-48', 'Mediano'), ('w-64', 'Grande'),
    ], default='w-48')
    autoplay = blocks.BooleanBlock(required=False, default=True)
    interval = blocks.IntegerBlock(required=False, default=5000)
    slides = blocks.ListBlock(HeroSlideBlock())

    class Meta:
        template = 'blocks/slider.html'
        icon = 'image'
        label = 'Slider Principal'

class StaticHeroBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=False)
    subtitle = blocks.TextBlock(required=False)

    class Meta:
        template = 'blocks/hero_estatico.html'
        icon = 'image'

class FeatureItemBlock(blocks.StructBlock):
    texto = blocks.CharBlock()
    icon_svg = blocks.TextBlock(required=False)

class TextWithImageBlock(blocks.StructBlock):
    image_position = blocks.ChoiceBlock(choices=[('right', 'Derecha'), ('left', 'Izquierda')], default='right')
    pre_title_highlight = blocks.CharBlock(required=False)
    pre_title_rest = blocks.CharBlock(required=False)
    main_heading = blocks.TextBlock()
    description = blocks.RichTextBlock()
    features_list = blocks.ListBlock(FeatureItemBlock(), required=False)
    image = ImageChooserBlock()
    button_text = blocks.CharBlock(required=False)
    button_link = blocks.URLBlock(required=False)
    class Meta:
        template = 'blocks/texto_con_imagen.html'
        icon = 'doc-empty-inverse'

class CategoryGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Nuestras categorías")
    class Meta:
        template = 'blocks/grilla_categorias.html'
        icon = 'list-ul'

class LogoCarouselBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Un mismo proveedor")
    subtitle = blocks.CharBlock(required=False)
    button_text = blocks.CharBlock(required=False)
    button_link = blocks.URLBlock(required=False)
    class Meta:
        template = 'blocks/carrusel_logos.html'
        icon = 'site'

class ReasonItemBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.TextBlock()

class NumberedFeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="¿Por qué elegirnos?")
    subtitle = blocks.CharBlock(required=False)
    reasons = blocks.ListBlock(ReasonItemBlock())
    class Meta:
        template = 'blocks/caracteristicas_numeradas.html'
        icon = 'list-ol'
        label = "Why Choose Us?"

class CardItemBlock(blocks.StructBlock):
    icon_upload = ImageChooserBlock(required=False)
    title = blocks.CharBlock()
    description = blocks.TextBlock()

class GridCardsBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Nuestros Valores")
    cards = blocks.ListBlock(CardItemBlock())
    class Meta:
        template = 'blocks/grilla_tarjetas.html'
        icon = 'table'

class CTABannerBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.TextBlock(required=False)
    class Meta:
        template = 'blocks/banner_texto.html'
        icon = 'title'

class FeaturedTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(features=['bold', 'italic', 'link'])
    alignment = blocks.ChoiceBlock(choices=[('text-left', 'Izquierda'), ('text-center', 'Centro'), ('text-right', 'Derecha')], default='text-center')
    style = blocks.ChoiceBlock(choices=[
        ('none', 'Limpio'),
        ('bg-grayAlt p-8 rounded-xl', 'Caja Gris'),
        ('bg-primary text-dark p-8 rounded-xl', 'Caja Amarilla'),
    ], default='none')
    class Meta:
        template = 'blocks/texto_destacado.html'
        icon = 'openquote'

class SimpleTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(features=['bold', 'italic', 'link'])
    alignment = blocks.ChoiceBlock(choices=[('text-left', 'Izquierda'), ('text-center', 'Centro'), ('text-right', 'Derecha')], default='text-center')
    size_lg = blocks.ChoiceBlock(
        choices=[
            ('text-lg', 'Pequeño (lg)'),           # 1.125rem / 18px
            ('text-xl', 'Mediano (xl)'),           # 1.25rem / 20px
            ('text-2xl', 'Grande (2xl)'),          # 1.5rem / 24px
            ('text-3xl', 'Extra Grande (3xl)'),    # 1.875rem / 30px
            ('text-4xl', '2XL (4xl)'),             # 2.25rem / 36px
            ('text-5xl', '3XL (5xl)'),             # 3rem / 48px
            ('text-6xl', '4XL (6xl)'),             # 3.75rem / 60px
        ],
        default='text-2xl',
        label="Tamaño en pantallas grandes (LG)"
    )
    class Meta:
        template = 'blocks/texto_simple.html'
        icon = 'title'

# ==========================================
# 3. LISTA DE BLOQUES Y PÁGINAS
# ==========================================

BLOQUES_COMUNES = [
    ('hero_estatico', StaticHeroBlock()),
    ('SeccionNostros', AboutUsBlock()), 
    ('SeccionBeneficio', MoreThanSupplierBlock()), 
    ('CategoriaProducto',CategoriesBlock()),
    ('texto_con_imagen', TextWithImageBlock()),
    ('layout_columnas', ColumnLayoutBlock()),
    ('titulo_personalizado', HeadingBlock()),
    ('boton_personalizado', ButtonBlock()),
    ('grilla_categorias', CategoryGridBlock()),
    ('grilla_tarjetas', GridCardsBlock()),
    ('caracteristicas_numeradas', NumberedFeaturesBlock()),
    ('Lista_de_marcas', BrandsCarouselBlock() ),
    ('banner_texto', CTABannerBlock()),
    ('texto_destacado', FeaturedTextBlock()),
    ('texto_simple', SimpleTextBlock()),
    ('BloqueMision', MissionBlock()),
    ('seccion_valores', ValuesBlock()),
    ('seccion_porque_elegir', WhyChooseShapinaBlock()),
    ('community_banner', CommunityBannerBlock()),
    ('FAQSection', FAQSectionBlock()),
    ('split_hero', SplitHeroBlock()),
    ('why_choose_us', WhyChooseUsBlock()),
    ('categories_section', CategoriesSectionBlock()),
    ('contact_section_dark', ContactSectionOscuroBlock()),
    ('contact_section_white', ContactSectionClaroBlock()),
    ('video_landing', VideoLandingBlock())
    
    

]

class HomePage(Page):
    body = StreamField([
        ('slider', SliderBlock()), 
    ] + BLOQUES_COMUNES, use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [FieldPanel('body')]

    def get_context(self, request):
        context = super().get_context(request)
        context['lista_categorias'] = Category.objects.all()
        context['lista_marcas'] = Brand.objects.all()
        return context

class StandardPage(Page):
    body = StreamField(BLOQUES_COMUNES, use_json_field=True, blank=True, null=True)
    content_panels = Page.content_panels + [FieldPanel('body')]