from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.snippets.blocks import SnippetChooserBlock

#############################################################

#FORMULARIO PARA HOME Y NOSOTROS ############################

#######################################################

class ContactSectionClaroBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=True, 
        default="Get in Touch with SaphinaGroup.com", 
        label="Título"
    )
    description = blocks.RichTextBlock(
        required=False, 
        label="Description",
        features=['bold', 'italic', 'link']
    )
    imagen = ImageChooserBlock(
        required=False, 
        label="Side Image",
        help_text="Upload the image that will accompany the form."
    )
    image_url = blocks.URLBlock(
        required=False,
        label=" image from URL",
        help_text="Paste a direct link to an image (e.g., https://example.com/image.jpg)."
    )


  
    def clean(self, value):
        result = super().clean(value)
        imagen = result.get('imagen')
        image_url = result.get('image_url')

     
        errors = {}

        # Regla 1: No pueden estar ambos vacíos
        if not imagen and not image_url:
            errors['imagen'] = ValidationError("You must select an image or provide a URL.")
            errors['image_url'] = ValidationError("You must provide a URL if you do not select an image.")

        # Regla 2: No pueden usar ambos al mismo tiempo
        if imagen and image_url:
            errors['image_url'] = ValidationError("Please, use only one method. Delete this URL if you use the top image.")

        # Si el diccionario tiene algo, lanzamos la excepción estructurada de Wagtail
        if errors:
            raise StructBlockValidationError(block_errors=errors)

        return result
    class Meta:
        template = 'blocks/contact_claro.html'
        icon = 'image'
        label = 'Contact Section (Clear with Image)'
        group = "Main Sections"

##SECCION DE CONTACTO OSCURO PARA LA PAGINA CONTACTO 

class ContactSectionOscuroBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=True, 
        default="Contact Us", 
        label="Title"
    )
    description = blocks.RichTextBlock(
        required=False, 
        label="Description",
        features=['bold', 'italic']
    )
    info_contacto = SnippetChooserBlock(
        'home.GlobalHeader', 
        label="Global Contact Information",
        help_text="Select the GlobalHeader that contains the company's address and phone number."
    )
    class Meta:
        template = 'blocks/contact_oscuro.html'
        icon = 'mail'
        label = 'section contact (dark)'
        group = "Main Sections"

###########################################################################

class CategoryItemBlockSecction(blocks.StructBlock):
    
    image = ImageChooserBlock(
        required=False, 
        label="Uploaded Image",
        help_text="Upload an image directly from your computer."
    )
    image_url = blocks.URLBlock(
        required=False, 
        label="Image URL",
        help_text="Alternatively, paste an external image URL here."
    )
    title = blocks.CharBlock(
        required=True, 
        label="Category Title"
    )

    def clean(self, value):
        result = super().clean(value)
        image = result.get('image')
        image_url = result.get('image_url')

        # Validation 1: At least one must be provided
        if not image and not image_url:
            errors = {
                'image': ValidationError("You must provide either an uploaded image or an image URL."),
                'image_url': ValidationError("You must provide either an uploaded image or an image URL.")
            }
            raise StructBlockValidationError(block_errors=errors)
        
        # Validation 2: They cannot provide both at the same time
        if image and image_url:
            errors = {
                'image': ValidationError("Please provide only ONE: either upload an image OR paste a URL, not both."),
                'image_url': ValidationError("Please provide only ONE: either upload an image OR paste a URL, not both.")
            }
            raise StructBlockValidationError(block_errors=errors)

        return result

    class Meta:
        icon = "tag"
        label = "Single Category"

class CategoriesSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True, 
        label="Main Title", 
        default="The Categories We Cover"
    )
    description = blocks.TextBlock(
        required=False, 
        label="Short Description", 
        default="Explore our diverse range of products, designed to meet the needs of our clients."
    )
    
    categories = blocks.ListBlock(
        CategoryItemBlockSecction(), 
        label="Category List"
    )

    class Meta:
        template = "blocks/categories_section_block.html"
        icon = "folder-open-inverse"
        label = "Categories Section"
        group = "Main Sections"
        




##Acordion Con Imagen##
class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Accordion Title")
    description = blocks.TextBlock(required=True, label="Description")

    class Meta:
        icon = "list-ul"
        label = "Accordion Element"

class WhyChooseUsBlock(blocks.StructBlock):
    subtitle = blocks.CharBlock(
        required=False, 
        label="Subtitle", 
        default="WHY CHOOSE US?"
    )
    title_part_1 = blocks.CharBlock(
        required=True, 
        label="Title (Main Part)", 
        default="Why Choose"
    )
    title_part_2 = blocks.CharBlock(
        required=True, 
        label="Title (Highlighted Part/Color)", 
        default="SaphinaGroup.Com?"
    )
    image = ImageChooserBlock(required=True, label="Main Image")
    
    # Lista dinámica para agregar tantos acordeones como se necesite
    accordion_items = blocks.ListBlock(
        AccordionItemBlock(), 
        label="Elementos del Acordeón"
    )

    class Meta:
        template = "blocks/why_choose_us_block.html" # Ajusta la ruta a tu proyecto
        icon = "help"
        label = "Why_choose_us_with_image"
        group = "Main Sections"




class CommunityBannerBlock(blocks.StructBlock):
    # Título principal (con soporte para salto de línea)
    title = blocks.CharBlock(
        required=True,
        default="Join our<br>community",
        help_text="Main title. Use <br> for line breaks."
    )
    # Subtítulo
    subtitle = blocks.CharBlock(
        required=True,
        default="The time has come to grow<br>your business!",
        help_text="Subtitle. Use <br> for line breaks."
    )
    # Párrafo descriptivo
    paragraph = blocks.TextBlock(
        required=True,
        default="At SaphinaGroup you will not only find exceptional products, but also a team committed to your success. Be part of our community of successful entrepreneurs in Latin America and the Caribbean.",
        help_text="Descriptive text. Line breaks are preserved automatically."
    )
    # Imagen (lado derecho)
    image = ImageChooserBlock(
        required=False,
        help_text="Upload an image to the right side"
    )
    image_url = blocks.URLBlock(
        required=False,
        help_text="Or use an external URL for the image"
    )
    # Opcional: ancho máximo del contenedor de texto (para mantener legibilidad)
    text_max_width = blocks.CharBlock(
        required=False,
        default="500px",
        help_text="Maximum width of the text block (e.g., 500px, 600px, 100%)"
    )

    def clean(self, value):
        if not value.get('image') and not value.get('image_url'):
            raise ValidationError("You must provide an image (by uploading a file or entering a URL)")
        return super().clean(value)

    class Meta:
        template = "blocks/community_banner_block.html"
        icon = "image"
        label = "Banner Comunidad"
        group = "Main Sections"


class WhyChooseShapinaBlock(blocks.StructBlock):
    # Imagen de la tarjeta (lado izquierdo)
    card_image = ImageChooserBlock(
        required=False,
        help_text="Upload an image for the card (horizontal format recommended)"
    )
    card_image_url = blocks.URLBlock(
        required=False,
        help_text="Or use an external URL for the image"
    )
    card_title = blocks.CharBlock(
        required=True,
        default="Why choose SaphinaGroup?",
        help_text="Title that appears above the image (you can use <br> for line break)"
    )
    
    titulo_right = blocks.CharBlock(default="When you join our Family", 
                                        label="Side Text",
                                        help_text="Title of the right side")
    resaltado_amarillo = blocks.CharBlock(default="you get",
                                           label="Yellow Text",
                                           help_text="Highlighted in yellow")
    
    # Lista de beneficios
    benefits = blocks.ListBlock(
    blocks.CharBlock(label="Benefit"),
    help_text="List of benefits (each with a yellow checkmark)"
)

    def clean(self, value):
        # Validar que al menos una opción de imagen esté presente
        if not value.get('card_image') and not value.get('card_image_url'):
            raise ValidationError("You must provide an image for the card (either upload a file or enter a URL")
        return super().clean(value)

    class Meta:
        template = "blocks/why_choose_saphina_block.html"
        icon = "image"
        label = "Why choose SaphineGroup?"
        group = "Main Sections"

#BLOQUE DE MISION 

class MissionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="Our Mission",
        help_text="Main title of the section"
    )
    description = blocks.TextBlock(
        required=True,
        help_text="Description / mission text"
    )
    image = ImageChooserBlock(
        required=True,
        help_text="Image that accompanies the text"
    )
    image_url = blocks.URLBlock(
        required=False,
        help_text="Or use an external URL for the image"
    )
    image_position = blocks.ChoiceBlock(
        choices=[
            ('right', 'Image on the right'),
            ('left', 'Image on the left'),
        ],
        default='right',
        help_text="Position of the image relative to the text"
    )
    def clean(self, value):
        if value.get('image') and value.get('image_url'):
            raise ValidationError("You must choose only one option: upload an image or enter a URL, not both.")
        if not value.get('image') and not value.get('image_url'):
            raise ValidationError("You must provide an image (either upload a file or enter a URL)")
        return super().clean(value)

    class Meta:
        template = "blocks/mission_block.html"
        icon = "image"
        label = "Mission / Vision Section"
        group = "Main Sections"

class ValueItemBlock(blocks.StructBlock):
    """Bloque para cada valor (tarjeta)"""
    icon = ImageChooserBlock(
        required=False,
        help_text="Upload an icon (SVG or PNG recommended)"
    )
    icon_url = blocks.URLBlock(
        required=False,
        help_text="Or use an external URL for the icon"
    )
    title = blocks.CharBlock(
        required=True,
        help_text="Value title (e.g., 'Quality')"
    )
    description = blocks.TextBlock(
        required=True,
        help_text="Value description"
    )

    def clean(self, value):
        # Validar que al menos uno de los dos campos de ícono esté completo
        if not value.get('icon') and not value.get('icon_url'):
            raise ValidationError("You must provide an icon (either upload an image or enter a URL)")
        return super().clean(value)

    class Meta:
        icon = "image"
        label = "Value"
        group = "Visual Components"




class ValuesBlock(blocks.StructBlock):
    """Bloque principal de la sección de valores"""
    title = blocks.CharBlock(
        required=True,
        default="Our Values",
        help_text="Main title (e.g., 'Our Values')"
    )
    subtitle_text = blocks.TextBlock(
        required=True,
        default="At SaphinaGroup, we are guided by a series of values that allow us to provide the best shopping experience for our customers. These values include:",
        help_text="Descriptive text that accompanies the title"
    )
    values = blocks.ListBlock(
        ValueItemBlock(),
        help_text="List of values (each with icon, title and description)"
    )

    class Meta:
        template = "blocks/values_block.html"
        icon = "list-ul"
        label = "Values Section"
        group = "Main Sections"

class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(label="Text")
    level = blocks.ChoiceBlock(choices=[
        ('h2', 'Large (H2)'),
        ('h3', 'Medium (H3)'),
        ('h4', 'Small (H4)'),
    ], default='h2')
    
    # CONTROL DE ESPACIADO (Padding/Margin)
    margin_top = blocks.ChoiceBlock(choices=[
        ('mt-0', 'No space'),
        ('mt-4', 'Small'),
        ('mt-8', 'Medium'),
        ('mt-12', 'Large'),
        ('mt-20', 'Extra Large'),
    ], default='mt-0', label="Margin Top")

    class Meta:
        template = 'blocks/atoms/heading.html'
        icon = 'title'
        label = 'Atomic Heading'

class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    link = blocks.URLBlock()
    style = blocks.ChoiceBlock(choices=[
        ('primary', 'Yellow'),
        ('dark', 'Black'),
        ('outline', 'Outline'),
    ], default='primary')

    class Meta:
        template = 'blocks/atoms/button.html'
        icon = 'link'

class BaseContentBlock(blocks.StreamBlock):
    """Here you put all the atoms you want to combine"""
    heading = HeadingBlock()
    paragraph = blocks.RichTextBlock(features=['bold', 'italic', 'link'])
    image = ImageChooserBlock()
    button = ButtonBlock()


class ColumnLayoutBlock(blocks.StructBlock):
    layout = blocks.ChoiceBlock(choices=[
        ('50_50', '2 Equal Columns'),
        ('33_66', 'Small Left'),
        ('66_33', 'Small Right'),
    ], default='50_50', label="Layout")

    # VERTICAL ALIGNMENT CONTROL (To align to top or center)
    vertical_align = blocks.ChoiceBlock(choices=[
        ('items-start', 'Top'),
        ('items-center', 'Middle'),
        ('items-end', 'Bottom'),
    ], default='items-start', label="Vertical Alignment")
    
    left_column = BaseContentBlock(label="Left Content")
    right_column = BaseContentBlock(label="Right Content")

    class Meta:
        template = 'blocks/layout_columns.html'
        icon = 'columns'
        label = 'Layout: Two Columns'

class AboutUsBlock(blocks.StructBlock):
   # Header (The one that says AquíLoHay | The ally...)
    resaltado_amarillo = blocks.CharBlock(default="SaphinaGroup", label="Yellow Text")
    texto_secundario = blocks.CharBlock(default=" | The ally your business needs", label="Side Text")
    
    # Left Column
    titulo_grande = blocks.RichTextBlock(features=['bold', 'italic'], label="Title (Use <br> for line breaks)")
    parrafos = blocks.RichTextBlock(label="Body text")
    beneficios = blocks.ListBlock(blocks.CharBlock(), label="Check Items", required=False)
    
    # Right Column
    imagen = ImageChooserBlock(label="Side Image")
    
    # Section Footer
    texto_pie = blocks.RichTextBlock(required=False, label="Text before button")
    boton_texto = blocks.CharBlock(required=False, label="Button text", help_text="E.g., Write to us on WhatsApp")
    whatsapp_numero = blocks.CharBlock(required=False, label="WhatsApp number", help_text="Include the country code without the + sign, e.g., +15615792949")
    whatsapp_mensaje = blocks.TextBlock(required=False, label="Default message", help_text="This text will appear ready to send in the chat.")

    class Meta:
        template = 'blocks/about_us_block.html'
        icon = 'group'
        label = 'Section: About Us (Rigid)'
        group = "Main Sections"

class MoreThanSupplierBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        help_text="Main title (e.g., 'We are more than a supplier')",
        default="We are more than a supplier"
    )
    intro_text = blocks.RichTextBlock(
        required=True,
        help_text="Introductory paragraph that appears before the list of benefits"
    )
    benefits = blocks.ListBlock(
        blocks.CharBlock(label="Benefit"),
        help_text="List of highlighted points (with checkmark)",
        label="Benefits list"
    )
    image = ImageChooserBlock(
        required=True,
        help_text="Image that appears on the left"
    )

    class Meta:
        template = "blocks/more_than_supplier_block.html"
        icon = "image"
        label = "More than a supplier"
        group = "Main Sections"



class CategoryItemBlock(blocks.StructBlock):
    name = blocks.CharBlock(
        required=True,
        help_text="Category name (you can use line breaks with \n)"
    )
    icon_image = ImageChooserBlock(
        required=False,
        help_text="Upload an image (SVG recommended) for the icon"
    )
    icon_url = blocks.URLBlock(
        required=False,
        help_text="Or use an external URL for the icon (e.g., https://example.com/icon.svg)"
    )
   

    def clean(self, value):
        # Validar que al menos uno de los dos campos de ícono esté completo
        if not value.get('icon_image') and not value.get('icon_url'):
            raise ValidationError("You must provide an icon (either upload an image or enter a URL)")
        return super().clean(value)

    class Meta:
        icon = "image"
        label = "Category"

class CategoriesBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="Our categories",
        help_text="Section title"
    )
    categories = blocks.ListBlock(
        CategoryItemBlock(),
        help_text="List of categories (you can add, remove and reorder)"
    )

    class Meta:
        template = "blocks/categories_block.html"
        icon = "list-ul"
        label = "Categories"
        group = "Main Sections"

class BrandLogoBlock(blocks.StructBlock):
    logo_image = ImageChooserBlock(
        required=False,
        help_text="Upload the brand logo (SVG or PNG recommended)"
    )
    logo_url = blocks.URLBlock(
        required=False,
        help_text="Or use an external URL for the logo"
    )
    alt_text = blocks.CharBlock(
        required=False,
        help_text="Alternative text for the image"
    )

    def clean(self, value):
        # Validar que al menos uno de los dos campos de logo esté completo
        if not value.get('logo_image') and not value.get('logo_url'):
            raise ValidationError("You must provide a logo (either upload an image or enter a URL)")
        return super().clean(value)

    class Meta:
        icon = "image"
        label = "Brand logo"



class BrandsCarouselBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="One single supplier,",
        help_text="Main title (e.g., 'One single supplier,')"
    )
    subtitle = blocks.CharBlock(
        required=True,
        default="access to 50 brands at the best price",
        help_text="Subtitle (e.g., 'access to 50 brands at the best price')"
    )
    brands = blocks.ListBlock(
        BrandLogoBlock(),
        help_text="List of brand logos that will appear in the carousel"
    )
    button_text = blocks.CharBlock(
        required=False,
        
    )
    button_url = blocks.URLBlock(
        required=False,
        help_text="Button URL"
    )

    class Meta:
        template = "blocks/brands_carousel_block.html"
        icon = "list-ul"
        label = "Brands carousel"
        group = "Main Sections"
#########################################################################

#FAQ ACCORDION

########################################################################
class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(label="Question")
    answer = blocks.RichTextBlock(
        label="Answer",
        features=['bold', 'italic', 'link', 'ul', 'ol']
    )

    class Meta:
        icon = 'help'


class FAQSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        default="Frequently Asked Questions",
        label="Section title"
    )
    subtitle = blocks.RichTextBlock(
        default="We answer your questions so you can focus on what matters: <b>growing your business.</b>",
        label="Subtitle",
        features=['bold', 'italic']
    )
    items = blocks.ListBlock(
        FAQItemBlock(),
        label="Questions and answers",
        min_num=1
    )

    class Meta:
        template = 'blocks/organisms/faq_section.html'
        icon = 'help'
        label = "FAQ Block"
        group = "Main Sections"

###############################################################
###Contact area hero########################
###############################################################

class SplitHeroBlock(blocks.StructBlock):
    pre_title = blocks.CharBlock(
        default="Connect with",
        required=False,
        label="Text before highlighted title"
    )
    highlighted_title = blocks.CharBlock(
        default="SaphinaGroup.com",
        required=True,
        label="Highlighted title (primary color)"
    )
    subtitle = blocks.TextBlock(
        default="Your trusted sourcing and distribution partner in Latin America",
        label="Subtitle"
    )
    bottom_image = ImageChooserBlock(
        required=True,
        label="Bottom image (e.g., truck, product)"
    )
    bg_color = blocks.CharBlock(
        default="#0d1117",
        required=False,
        label="Background color",
        help_text="HEX code for dark background"
    )
    
    # Optional: height
    height = blocks.ChoiceBlock(
        choices=[
            ('70', '70vh'),
            ('85', '85vh (default)'),
        ],
        default='85',
        label="Minimum height"
    )

    class Meta:
        template = 'blocks/organisms/split_hero.html'
        icon = 'image'
        label = "Hero with bottom image"
        group = "Main Sections"


class VideoLandingBlock(blocks.StructBlock):
    # --- HERO VIDEO ---
    logo = ImageChooserBlock(required=False, label="Logo")
    titulo_principal = blocks.RichTextBlock(features=['bold', 'italic'], label="Main Title")
    banner_video_text = blocks.CharBlock(default="Click the 'PLAY' button and discover how to work with us!", label="Video Banner Text")
    
    # --- LEAD MAGNET MAGIC ---
    video_thumbnail = ImageChooserBlock(label="Video Thumbnail (Before form)")
    actual_video_embed = blocks.URLBlock(label="Actual Video URL", help_text="e.g., YouTube Embed URL. Shown after filling the form.")
    form_webhook = blocks.URLBlock(required=False, label="Webhook URL (For leads)", help_text="e.g., Zapier, Make, or CRM URL")
    tiempo_aparicion = blocks.IntegerBlock(default=15, label="Seconds to show modal automatically")
    
    boton_video_text = blocks.CharBlock(default="Watch the Video!", label="Video Button Text")

    # --- BIO ---
    banner_bio_text = blocks.CharBlock(default="Click here and discover how to work with us NOW!", label="Bio Banner Text")
    bio_image = ImageChooserBlock(label="Profile Picture")
    bio_nombre = blocks.CharBlock(default="Saphinagroup", label="Name")
    bio_cargo = blocks.CharBlock(default="", label="Role/Subtitle")
    bio_descripcion = blocks.RichTextBlock(label="Bio Description")
    boton_final_text = blocks.CharBlock(default="Watch the Video!", label="Final Button Text")

    class Meta:
        template = 'home/blocks/video_landing.html'
        icon = 'media'
        label = 'Landing: Gated Video'
        group = "Main Sections"