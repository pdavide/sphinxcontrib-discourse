"""Sphinx extension that embeds Discourse topics in documents."""

from __future__ import print_function
import os
import re
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.errors import ExtensionError, SphinxError

__author__ = 'Team per la Trasformazione Digitale'
__license__ = 'BSD-3-clause'
__version__ = '0.0.1'


class DiscourseError(SphinxError):
    """Non-configuration error. Raised when directive has bad options."""

    category = 'Discourse option error'


class DiscourseNode(nodes.General, nodes.Element):
    """Discourse <div /> node for Sphinx/docutils."""
    
    def __init__(self, topic_identifier):
        """Store directive options during instantiation.
        :param str disqus_shortname: Required Disqus forum name identifying the website.
        :param str disqus_identifier: Unique identifier for each page where Disqus is present.
        """
        super(DiscourseNode, self).__init__()
        self.topic_identifier = topic_identifier
    
    def get_topic_identifier(self):
        return self.topic_identifier;

    @staticmethod
    def visit(self, node):
        """Append div placeholder to document body list."""
        self.body.append('<div id ="discourse-comments"></div>')

    @staticmethod
    def depart(self, node):
        pass


class DiscourseDirective(Directive):
    """Discourse ".. discourse::" rst directive."""

    option_spec = dict(topic_identifier=str)

    def get_topic_identifier(self):
        """Validate and returns topic_identifier option value.

        :returns: topic_identifier config value.
        :rtype: str
        """
        if 'topic_identifier' in self.options:
            return self.options['topic_identifier']
        else:
            raise DiscourseError('No :topic_identifier: option found in ::discourse: directive.')

    def run(self):
        """Executed by Sphinx.

        :returns: Single DiscourseNode instance.
        :rtype: list
        """

        if self.state.document.traverse(DiscourseNode):
            raise DiscourseError('::discourse: directive found more than once in the same file.')
        discourse_topic_identifier = self.get_topic_identifier()
        env = self.state.document.settings.env
        current_builder = env.app.builder.name
        if current_builder == 'html' or current_builder == 'readthedocs':
            return [DiscourseNode(discourse_topic_identifier)]
        return []


def event_html_page_context(app, pagename, templatename, context, doctree):
    """Called when the HTML builder has created a context dictionary to render a template with.

    Conditionally appending required js snippet to <body> if the directive is used in a page.

    :param sphinx.application.Sphinx app: Sphinx application object.
    :param str pagename: Name of the page being rendered (without .html or any file extension).
    :param str templatename: Page name with .html.
    :param dict context: Jinja2 HTML context.
    :param docutils.nodes.document doctree: Tree of docutils nodes.
    """

    reURL = re.compile('^https?://\S+/$')
    current_builder = app.builder.name
    if current_builder == 'html' or current_builder == 'readthedocs':
        if doctree and doctree.traverse(DiscourseNode):
            if not app.config.discourse_url:
                raise DiscourseError('::discourse: directive found, but discourse_url is not set in conf.py')
            if not reURL.match(app.config.discourse_url):
                raise DiscourseError('::discourse: directive found, but discourse_url is not set properly in conf.py (must be a valid URL starting with http:// or https:// and ending with trailing slash)')
            for discourse_node in doctree.traverse(DiscourseNode):
                context['body'] += """<script type='text/javascript'>
                                        DiscourseEmbed = { discourseUrl: '%s',
                                        topicId: '%s' };
                                        (function() {
                                            var d = document.createElement('script'); d.type = 'text/javascript'; d.async = true;
                                            d.src = DiscourseEmbed.discourseUrl + 'javascripts/embed.js';
                                            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(d);
                                        })();
                                   </script>""" % (app.config.discourse_url, discourse_node.get_topic_identifier())


def setup(app):
    """Called by Sphinx during phase 0 (initialization).

    :param app: Sphinx application object.

    :returns: Extension version.
    :rtype: dict
    """
    app.add_config_value('discourse_url', None, 'html')
    app.add_directive('discourse', DiscourseDirective)
    app.add_node(DiscourseNode,
                 html=(DiscourseNode.visit, DiscourseNode.depart),
                 latex=(DiscourseNode.visit, DiscourseNode.depart),
                 text=(DiscourseNode.visit, DiscourseNode.depart))
    app.connect('html-page-context', event_html_page_context)
    return {'version': __version__}
