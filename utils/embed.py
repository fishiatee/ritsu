from interactions import Embed, Color, EmbedAttachment, EmbedAuthor, EmbedFooter, EmbedField

class EmbedBuilder:
    header: str
    header_image_url: str
    header_url: str
    thumbnail_image_url: str
    images: list[EmbedAttachment]
    title: str
    title_url: str
    contents: str
    color: Color
    footer: str
    footer_image_url: str
    fields: list[EmbedField]
    def __init__(self):
        self.header = ""
        self.header_image_url = ""
        self.header_url = ""
        self.thumbnail_image_url = ""
        self.images = []
        self.title = ""
        self.title_url = ""
        self.contents = ""
        self.color = ""
        self.footer = ""
        self.footer_image_url = ""
        self.fields = []
    def build(self) -> Embed:
        return Embed(
            title=self.title,
            url=self.title_url,
            description=self.contents,
            color=self.color,
            author=EmbedAuthor(
                name=self.header,
                icon_url=self.header_image_url,
                url=self.header_url
            ),
            thumbnail=self.thumbnail_image_url,
            images=self.images,
            footer=EmbedFooter(
                text=self.footer,
                icon_url=self.footer_image_url
            ),
            fields=self.fields
        )
    def construct_from(self, embed: Embed):
        self.header = embed.author.name
        self.header_image_url = embed.author.icon_url
        self.header_url = embed.author.url
        self.thumbnail_image_url = embed.thumbnail
        self.images = embed.images
        self.title = embed.title
        self.title_url = embed.url
        self.contents = embed.description
        self.color = embed.color
        self.footer = embed.footer.text
        self.footer_image_url = embed.footer.icon_url
        self.fields = embed.fields
    def set_header(self, text: str, image_url: str = None, url: str = None):
        self.header = text
        self.header_image_url = image_url
        self.header_url = url
    def set_footer(self, text: str, image_url: str = None):
        self.footer = text
        self.footer_image_url = image_url
    def set_thumbnail_image(self, url: str):
        self.thumbnail_image_url = url
    def add_image(self, url: str):
        self.images.append(EmbedAttachment(
            url=url
        ))
    def set_title(self, title: str, url: str = None):
        self.title = title
        self.title_url = url
    def set_color(self, color: str):
        self.color = Color.from_hex(color)
    def add_content(self, msg: str, new_line: bool = True):
        if not self.contents:
            self.contents = ""
        self.contents += msg
        if new_line:
            self.contents += "\n"
    def clear_content(self):
        self.contents = ""
    def add_field(self, title: str, content: str, inline: bool = False) -> int:
        field = EmbedField(
            name=title,
            value=content,
            inline=inline
        )
        self.fields.append(field)
        return self.fields.index(field)
    def edit_field(self, index: int, title: str, content: str, inline: bool = False):
        self.fields[index] = EmbedField(
            name=title,
            value=content,
            inline=inline
        )