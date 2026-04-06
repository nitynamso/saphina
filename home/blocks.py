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
        label="Descripción",
        features=['bold', 'italic', 'link']
    )
    imagen = ImageChooserBlock(
        required=False, 
        label="Imagen lateral",
        help_text="Sube la imagen que acompañará al formulario."
    )
    image_url = blocks.URLBlock(
        required=False,
        label=" image from URL",
        help_text="Pega un enlace directo a una imagen (ej: https://example.com/imagen.jpg)."
    )


  
    def clean(self, value):
        result = super().clean(value)
        imagen = result.get('imagen')
        image_url = result.get('image_url')

     
        errors = {}

        # Regla 1: No pueden estar ambos vacíos
        if not imagen and not image_url:
            errors['imagen'] = ValidationError("Debes seleccionar una imagen o proporcionar una URL.")
            errors['image_url'] = ValidationError("Debes proporcionar una URL si no seleccionas una imagen.")

        # Regla 2: No pueden usar ambos al mismo tiempo
        if imagen and image_url:
            errors['image_url'] = ValidationError("Por favor, usa solo un método. Borra esta URL si usas la imagen superior.")

        # Si el diccionario tiene algo, lanzamos la excepción estructurada de Wagtail
        if errors:
            raise StructBlockValidationError(block_errors=errors)

        return result
    class Meta:
        template = 'blocks/contact_claro.html'
        icon = 'image'
        label = 'Sección Contacto (Claro con Imagen)'
        group = "Secciones Principales"

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
        label="Información de Contacto Global",
        help_text="Selecciona el GlobalHeader que contiene la dirección y teléfono de la empresa."
    )
    class Meta:
        template = 'blocks/contact_oscuro.html'
        icon = 'mail'
        label = 'section contact (dark)'
        group = "Secciones Principales"

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
        group = "Secciones Principales"
        




##Acordion Con Imagen##
class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label="Título del Acordeón")
    description = blocks.TextBlock(required=True, label="Descripción")

    class Meta:
        icon = "list-ul"
        label = "Elemento de Acordeón"

class WhyChooseUsBlock(blocks.StructBlock):
    subtitle = blocks.CharBlock(
        required=False, 
        label="Subtítulo", 
        default="¿POR QUÉ ELEGIRNOS?"
    )
    title_part_1 = blocks.CharBlock(
        required=True, 
        label="Título (Parte Principal)", 
        default="¿Por Qué Elegir"
    )
    title_part_2 = blocks.CharBlock(
        required=True, 
        label="Título (Parte Destacada/Color)", 
        default="AquíLoHay.Com?"
    )
    image = ImageChooserBlock(required=True, label="Imagen Principal")
    
    # Lista dinámica para agregar tantos acordeones como se necesite
    accordion_items = blocks.ListBlock(
        AccordionItemBlock(), 
        label="Elementos del Acordeón"
    )

    class Meta:
        template = "blocks/why_choose_us_block.html" # Ajusta la ruta a tu proyecto
        icon = "help"
        label = "Why_choose_us_with_image"
        group = "Secciones Principales"




class CommunityBannerBlock(blocks.StructBlock):
    # Título principal (con soporte para salto de línea)
    title = blocks.CharBlock(
        required=True,
        default="Únete a nuestra<br>comunidad",
        help_text="Título principal. Usa <br> para saltos de línea."
    )
    # Subtítulo
    subtitle = blocks.CharBlock(
        required=True,
        default="¡Llegó el momento de hacer<br>crecer tu negocio!",
        help_text="Subtítulo. Usa <br> para saltos de línea."
    )
    # Párrafo descriptivo
    paragraph = blocks.TextBlock(
        required=True,
        default="En SaphinaGroup no solo encontrarás productos excepcionales, sino un equipo comprometido con tu éxito. Forma parte de nuestra comunidad de emprendedores exitosos en América Latina y el Caribe.",
        help_text="Texto descriptivo. Los saltos de línea se conservan automáticamente."
    )
    # Imagen (lado derecho)
    image = ImageChooserBlock(
        required=False,
        help_text="Sube una imagen para el lado derecho"
    )
    image_url = blocks.URLBlock(
        required=False,
        help_text="O usa una URL externa para la imagen"
    )
    # Opcional: ancho máximo del contenedor de texto (para mantener legibilidad)
    text_max_width = blocks.CharBlock(
        required=False,
        default="500px",
        help_text="Ancho máximo del bloque de texto (ej: 500px, 600px, 100%)"
    )

    def clean(self, value):
        if not value.get('image') and not value.get('image_url'):
            raise ValidationError("Debes proporcionar una imagen (subiendo un archivo o ingresando una URL)")
        return super().clean(value)

    class Meta:
        template = "blocks/community_banner_block.html"
        icon = "image"
        label = "Banner Comunidad"
        group = "Secciones Principales"


class WhyChooseShapinaBlock(blocks.StructBlock):
    # Imagen de la tarjeta (lado izquierdo)
    card_image = ImageChooserBlock(
        required=False,
        help_text="Sube una imagen para la tarjeta (recomendado formato horizontal)"
    )
    card_image_url = blocks.URLBlock(
        required=False,
        help_text="O usa una URL externa para la imagen"
    )
    card_title = blocks.CharBlock(
        required=True,
        default="¿Por qué elegir a SaphinaGroup?",
        help_text="Título que aparece sobre la imagen (puedes usar <br> para salto de línea)"
    )
    
    titulo_right = blocks.CharBlock(default="Cuando te unes a nuestra Familia", 
                                        label="Texto al lado",
                                        help_text="Titulo del lado derecho")
    resaltado_amarillo = blocks.CharBlock(default="obtienes",
                                           label="Texto Amarillo",
                                           help_text="Resaltado en amarillo")
    
    # Lista de beneficios
    benefits = blocks.ListBlock(
        blocks.CharBlock(label="Beneficio"),
        help_text="Lista de beneficios (cada uno con un check amarillo)"
    )

    def clean(self, value):
        # Validar que al menos una opción de imagen esté presente
        if not value.get('card_image') and not value.get('card_image_url'):
            raise ValidationError("Debes proporcionar una imagen para la tarjeta (subiendo un archivo o ingresando una URL)")
        return super().clean(value)

    class Meta:
        template = "blocks/why_choose_saphina_block.html"
        icon = "image"
        label = "¿Por qué elegir SaphineGroup?"  
        group = "Secciones Principales"

#BLOQUE DE MISION 
class MissionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="Nuestra Misión",
        help_text="Título principal de la sección"
    )
    description = blocks.TextBlock(
        required=True,
        help_text="Descripción / texto de la misión"
    )
    image = ImageChooserBlock(
        required=True,
        help_text="Imagen que acompaña al texto"
    )
    image_url = blocks.URLBlock(
        required=False,
        help_text="O usa una URL externa para la imagen"
    )
    image_position = blocks.ChoiceBlock(
        choices=[
            ('right', 'Imagen a la derecha'),
            ('left', 'Imagen a la izquierda'),
        ],
        default='right',
        help_text="Posición de la imagen respecto al texto"
    )
    def clean(self, value):
        if value.get('image') and value.get('image_url'):
            raise ValidationError("Debes elegir solo una opción: subir una imagen o ingresar una URL, no ambas.")
        if not value.get('image') and not value.get('image_url'):
            raise ValidationError("Debes proporcionar una imagen (subiendo un archivo o ingresando una URL)")
        return super().clean(value)

    class Meta:
        template = "blocks/mission_block.html"
        icon = "image"
        label = "Sección Misión / Visión"
        group = "Secciones Principales"



class ValueItemBlock(blocks.StructBlock):
    """Bloque para cada valor (tarjeta)"""
    icon = ImageChooserBlock(
        required=False,
        help_text="Sube un ícono (recomendado SVG o PNG)"
    )
    icon_url = blocks.URLBlock(
        required=False,
        help_text="O usa una URL externa para el ícono"
    )
    title = blocks.CharBlock(
        required=True,
        help_text="Título del valor (ej: 'Calidad')"
    )
    description = blocks.TextBlock(
        required=True,
        help_text="Descripción del valor"
    )

    def clean(self, value):
        # Validar que al menos uno de los dos campos de ícono esté completo
        if not value.get('icon') and not value.get('icon_url'):
            raise ValidationError("Debes proporcionar un ícono (subiendo una imagen o ingresando una URL)")
        return super().clean(value)

    class Meta:
        icon = "image"
        label = "Valor"
        group = "Componentes Visuales"  # opcional: agrupar


class ValuesBlock(blocks.StructBlock):
    """Bloque principal de la sección de valores"""
    title = blocks.CharBlock(
        required=True,
        default="Nuestros Valores",
        help_text="Título principal (ej: 'Nuestros Valores')"
    )
    subtitle_text = blocks.TextBlock(
        required=True,
        default="En AquíLohay, nos guiamos por una serie de valores que nos permiten brindar la mejor experiencia de compra para nuestros clientes. Estos valores incluyen:",
        help_text="Texto descriptivo que acompaña al título"
    )
    values = blocks.ListBlock(
        ValueItemBlock(),
        help_text="Lista de valores (cada uno con ícono, título y descripción)"
    )

    class Meta:
        template = "blocks/values_block.html"
        icon = "list-ul"
        label = "Sección Valores"
        group = "Secciones Principales"  


class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(label="Texto")
    level = blocks.ChoiceBlock(choices=[
        ('h2', 'Grande (H2)'),
        ('h3', 'Mediano (H3)'),
        ('h4', 'Pequeño (H4)'),
    ], default='h2')
    
    # CONTROL DE ESPACIADO (Padding/Margin)
    margin_top = blocks.ChoiceBlock(choices=[
        ('mt-0', 'Sin espacio'),
        ('mt-4', 'Pequeño'),
        ('mt-8', 'Mediano'),
        ('mt-12', 'Grande'),
        ('mt-20', 'Extra Grande'),
    ], default='mt-0', label="Espacio Superior")

    class Meta:
        template = 'blocks/atoms/heading.html'
        icon = 'title'
        label = 'Título Atómico'

class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    link = blocks.URLBlock()
    style = blocks.ChoiceBlock(choices=[
        ('primary', 'Amarillo'),
        ('dark', 'Negro'),
        ('outline', 'Borde'),
    ], default='primary')

    class Meta:
        template = 'blocks/atoms/button.html'
        icon = 'link'

class BaseContentBlock(blocks.StreamBlock):
    """Aquí metes todos los átomos que quieras combinar"""
    heading = HeadingBlock()
    paragraph = blocks.RichTextBlock(features=['bold', 'italic', 'link'])
    image = ImageChooserBlock()
    button = ButtonBlock()


class ColumnLayoutBlock(blocks.StructBlock):
    layout = blocks.ChoiceBlock(choices=[
        ('50_50', '2 Columnas Iguales'),
        ('33_66', 'Izquierda Pequeña'),
        ('66_33', 'Derecha Pequeña'),
    ], default='50_50', label="Distribución")

    # CONTROL DE ALINEACIÓN VERTICAL (Para llevar al top o centro)
    vertical_align = blocks.ChoiceBlock(choices=[
        ('items-start', 'Arriba (Top)'),
        ('items-center', 'Centrado (Middle)'),
        ('items-end', 'Abajo (Bottom)'),
    ], default='items-start', label="Alineación Vertical")
    
    left_column = BaseContentBlock(label="Contenido Izquierda")
    right_column = BaseContentBlock(label="Contenido Derecha")

    class Meta:
        template = 'blocks/layout_columns.html'
        icon = 'columns'
        label = 'Layout: Dos Columnas'

class AboutUsBlock(blocks.StructBlock):
   # Encabezado (El que dice AquíLoHay | El aliado...)
    resaltado_amarillo = blocks.CharBlock(default="AquíLoHay", label="Texto Amarillo")
    texto_secundario = blocks.CharBlock(default=" | El aliado que tu negocio necesita", label="Texto al lado")
    
    # Columna Izquierda
    titulo_grande = blocks.RichTextBlock(features=['bold', 'italic'], label="Título (Usa <br> para saltos)")
    parrafos = blocks.RichTextBlock(label="Cuerpo de texto")
    beneficios = blocks.ListBlock(blocks.CharBlock(), label="Items con Check", required=False)
    
    # Columna Derecha
    imagen = ImageChooserBlock(label="Imagen Lateral")
    
    # Pie de Sección
    texto_pie = blocks.RichTextBlock(required=False, label="Texto antes del botón")
    boton_texto = blocks.CharBlock(required=False, label="Texto del botón")
    boton_url = blocks.URLBlock(required=False, label="Link del botón")

    class Meta:
        template = 'blocks/about_us_block.html'
        icon = 'group'
        label = 'Sección: Sobre Nosotros (Rígido)'
        group = "Secciones Principales"

class MoreThanSupplierBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        help_text="Título principal (ej: 'Somos más que un proveedor')",
        default="Somos más que un proveedor"
    )
    intro_text = blocks.RichTextBlock(
        required=True,
        help_text="Párrafo introductorio que aparece antes de la lista de beneficios"
    )
    benefits = blocks.ListBlock(
        blocks.CharBlock(label="Beneficio"),
        help_text="Lista de puntos destacados (con check)",
        label="Lista de beneficios"
    )
    image = ImageChooserBlock(
        required=True,
        help_text="Imagen que aparece a la izquierda"
    )

    class Meta:
        template = "blocks/more_than_supplier_block.html"
        icon = "image"
        label = "Más que un proveedor"
        group = "Secciones Principales"



class CategoryItemBlock(blocks.StructBlock):
    name = blocks.CharBlock(
        required=True,
        help_text="Nombre de la categoría (puedes usar saltos de línea con \n)"
    )
    icon_image = ImageChooserBlock(
        required=False,
        help_text="Sube una imagen (recomendado SVG) para el ícono"
    )
    icon_url = blocks.URLBlock(
        required=False,
        help_text="O usa una URL externa para el ícono (ej: https://ejemplo.com/icono.svg)"
    )
   

    def clean(self, value):
        # Validar que al menos uno de los dos campos de ícono esté completo
        if not value.get('icon_image') and not value.get('icon_url'):
            raise ValidationError("Debes proporcionar un ícono (subiendo una imagen o ingresando una URL)")
        return super().clean(value)

    class Meta:
        icon = "image"
        label = "Categoría"

class CategoriesBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="Nuestras categorías",
        help_text="Título de la sección"
    )
    categories = blocks.ListBlock(
        CategoryItemBlock(),
        help_text="Lista de categorías (puedes añadir, eliminar y ordenar)"
    )

    class Meta:
        template = "blocks/categories_block.html"
        icon = "list-ul"
        label = "Categorías"
        group = "Secciones Principales"

class BrandLogoBlock(blocks.StructBlock):
    logo_image = ImageChooserBlock(
        required=False,
        help_text="Sube el logo de la marca (recomendado SVG o PNG)"
    )
    logo_url = blocks.URLBlock(
        required=False,
        help_text="O usa una URL externa para el logo"
    )
    alt_text = blocks.CharBlock(
        required=False,
        help_text="Texto alternativo para la imagen"
    )

    def clean(self, value):
        # Validar que al menos uno de los dos campos de logo esté completo
        if not value.get('logo_image') and not value.get('logo_url'):
            raise ValidationError("Debes proporcionar un logo (subiendo una imagen o ingresando una URL)")
        return super().clean(value)

    class Meta:
        icon = "image"
        label = "Logo de marca"



class BrandsCarouselBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        default="Un mismo proveedor,",
        help_text="Título principal (ej: 'Un mismo proveedor,')"
    )
    subtitle = blocks.CharBlock(
        required=True,
        default="acceso a 50 marcas al mejor precio",
        help_text="Subtítulo (ej: 'acceso a 50 marcas al mejor precio')"
    )
    brands = blocks.ListBlock(
        BrandLogoBlock(),
        help_text="Lista de logos de marcas que aparecerán en el carrusel"
    )
    button_text = blocks.CharBlock(
        required=True,
        default="Descubre nuestro catálogo"
    )
    button_url = blocks.URLBlock(
        required=True,
        help_text="URL del botón"
    )

    class Meta:
        template = "blocks/brands_carousel_block.html"
        icon = "list-ul"
        label = "Carrusel de marcas"
        group = "Secciones Principales"
#########################################################################

#ACORDION DE PREGUNTAS FRECUENTES

########################################################################
class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(label="Pregunta")
    answer = blocks.RichTextBlock(
        label="Respuesta",
        features=['bold', 'italic', 'link', 'ul', 'ol']
    )

    class Meta:
        icon = 'help'


class FAQSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        default="Preguntas Frecuentes",
        label="Título de la sección"
    )
    subtitle = blocks.RichTextBlock(
        default="Resolvemos tus dudas para que puedas enfocarte en lo que importa: <b>hacer crecer tu negocio.</b>",
        label="Subtítulo",
        features=['bold', 'italic']
    )
    items = blocks.ListBlock(
        FAQItemBlock(),
        label="Preguntas y respuestas",
        min_num=1
    )

    class Meta:
        template = 'blocks/organisms/faq_section.html'
        icon = 'help'
        label = "FAQ Block"
        group = "Secciones Principales"

###############################################################
###Hero del area contacto################
###############################################################

class SplitHeroBlock(blocks.StructBlock):
    pre_title = blocks.CharBlock(
        default="Connect with",
        required=False,
        label="Texto antes del título destacado"
    )
    highlighted_title = blocks.CharBlock(
        default="SaphinaGroup.com",
        required=True,
        label="Título destacado (color primary)"
    )
    subtitle = blocks.TextBlock(
        default="Your trusted sourcing and distribution partner in Latin America",
        label="Subtítulo"
    )
    bottom_image = ImageChooserBlock(
        required=True,
        label="Imagen inferior (ej: camión, producto)"
    )
    bg_color = blocks.CharBlock(
        default="#0d1117",
        required=False,
        label="Color de fondo",
        help_text="Código HEX del fondo oscuro"
    )
    
    # Opcional: altura
    height = blocks.ChoiceBlock(
        choices=[
            ('70', '70vh'),
            ('85', '85vh (default)'),
        ],
        default='85',
        label="Altura mínima"
    )

    class Meta:
        template = 'blocks/organisms/split_hero.html'
        icon = 'image'
        label = "Hero con imagen inferior"
        group = "Secciones Principales"