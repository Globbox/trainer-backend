from django.forms.widgets import Textarea


class MarkdownWidget(Textarea):
    """Widget дял Markdown."""

    template_name = 'widgets/markdown_widget.html'

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js',
        )
