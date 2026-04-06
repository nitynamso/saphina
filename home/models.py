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
    Central header control: Logo and Top Banner.
    Affects the entire site simultaneously.
    """
    title = models.CharField(max_length=255, default="Header Configuration")
    
    # --- LOGO ---
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Main Logo"
    )
    logo_width = models.IntegerField(
        default=100, 
        verbose_name="Logo Width (px)",
        help_text="Adjust the logo size in the header"
    )

    # --- TOP BAR (BANNER) ---
    address = models.CharField(max_length=255, default="13463 N W 19th Lane, Miami, FL 33182", verbose_name="Address")
    phone = models.CharField(max_length=50, default="+1 (786) 847-5568", verbose_name="Phone")
    
    # --- STYLES ---
    bg_color = models.CharField(max_length=7, default="#FAD02C", verbose_name="Banner Background Color (Hex)")
    text_color = models.CharField(max_length=7, default="#1a1a1a", verbose_name="Banner Text Color (Hex)")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('logo_width'),
        ], heading="Branding / Logo"),
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone'),
        ], heading="Top Banner Information"),
        MultiFieldPanel([
            FieldPanel('bg_color'),
            FieldPanel('text_color'),
        ], heading="Banner Styles"),
    ]

    def __str__(self):
        return self.title

    def get_preview_template(self, request, mode_name):
        return "includes/header_preview.html"

    def get_preview_context(self, request, mode_name):
        return {"header": self}


@register_setting
class SiteSettings(BaseSiteSetting):
    """Social media settings."""
    facebook = models.URLField(blank=True, help_text="Facebook URL")
    instagram = models.URLField(blank=True, help_text="Instagram URL")
    web3forms_key = models.CharField(
        max_length=100, 
        verbose_name="Web3Forms Key",
        help_text="Paste your Access Key here. This will activate all contact forms on the website.",
        default="Sin Llave",
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('web3forms_key')
        ], heading="General Settings"),
    ]





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
    autoplay = blocks.BooleanBlock(required=False, default=True)
    interval = blocks.IntegerBlock(required=False, default=5000)
    slides = blocks.ListBlock(HeroSlideBlock())

    class Meta:
        template = 'blocks/slider.html'
        icon = 'image'
        label = 'Main Slider'
        group = "Main Sections"

class StaticHeroBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=False)
    subtitle = blocks.TextBlock(required=False)

    class Meta:
        template = 'blocks/hero_estatico.html'
        icon = 'image'
        group = "Main Sections"

class FeatureItemBlock(blocks.StructBlock):
    texto = blocks.CharBlock()
    icon_svg = blocks.TextBlock(required=False)

class TextWithImageBlock(blocks.StructBlock):
    image_position = blocks.ChoiceBlock(choices=[('right', 'Right'), ('left', 'Left')], default='right')
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
        label = 'Text with image'

class CategoryGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Our categories")
    class Meta:
        template = 'blocks/grilla_categorias.html'
        icon = 'list-ul'
        

class LogoCarouselBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="One single supplier")
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
    title = blocks.CharBlock(default="Why choose us?")
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
    title = blocks.CharBlock(default="Our Values")
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
    alignment = blocks.ChoiceBlock(choices=[('text-left', 'Left'), ('text-center', 'Center'), ('text-right', 'Right')], default='text-center')
    style = blocks.ChoiceBlock(choices=[
        ('none', 'Clean'),
        ('bg-grayAlt p-8 rounded-xl', 'Gray Box'),
        ('bg-primary text-dark p-8 rounded-xl', 'Yellow Box'),
    ], default='none')
    class Meta:
        template = 'blocks/texto_destacado.html'
        icon = 'openquote'
class SimpleTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(features=['bold', 'italic', 'link'])
    alignment = blocks.ChoiceBlock(choices=[('text-left', 'Left'), ('text-center', 'Center'), ('text-right', 'Right')], default='text-center')
    size_lg = blocks.ChoiceBlock(
        choices=[
            ('text-lg', 'Small (lg)'),           # 1.125rem / 18px
            ('text-xl', 'Medium (xl)'),           # 1.25rem / 20px
            ('text-2xl', 'Large (2xl)'),          # 1.5rem / 24px
            ('text-3xl', 'Extra Large (3xl)'),    # 1.875rem / 30px
            ('text-4xl', '2XL (4xl)'),             # 2.25rem / 36px
            ('text-5xl', '3XL (5xl)'),             # 3rem / 48px
            ('text-6xl', '4XL (6xl)'),             # 3.75rem / 60px
        ],
        default='text-2xl',
        label="Size on large screens (LG)"
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

    

class StandardPage(Page):
    body = StreamField(BLOQUES_COMUNES, use_json_field=True, blank=True, null=True)
    content_panels = Page.content_panels + [FieldPanel('body')]