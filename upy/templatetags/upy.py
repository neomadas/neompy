from django.template import Library, Node
from django.template.base import FilterExpression, Parser, Token
from django.template.loader_tags import construct_relative_path


register = Library()


class UpyImportNode(Node):

  def __init__(self, template: FilterExpression, *args, **kwargs):
    self.template = template
    super().__init__(*args, **kwargs)

  def render(self, context):
    subpath = self.template.resolve(context)
    fullpath = (construct_relative_path(self.origin.template_name, subpath),)

    cache = context.render_context.dicts[0].setdefault(self, {})
    template = cache.get(fullpath)

    if not template:
      template = context.template.engine.select_template(fullpath)
      cache[fullpath] = template

    return template.render(context)


@register.tag
def upy_import(parser: Parser, token: Token):
  bits = token.split_contents()
  if len(bits) < 2:
    raise template.TemplateSyntaxError(
      f'{bits[0]} tag takes at least one argument: the asset path')
  bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
  return UpyImportNode(parser.compile_filter(bits[1]))
