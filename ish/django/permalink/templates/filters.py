from django import template
from django.core.urlresolvers import reverse, get_resolver, get_callable
from django.template import TemplateSyntaxError
register = template.Library()

def permalink(object, url=None):
    '''Django template engine filter. Provides a permalink filter to ensure
    presentation layer is decoupled from model.
    
        v0.2 - 06/04/2009
            IS: Initial Release
    
    Usage:
            {{ my_model|permalink }}
            
    By default, the filter will lookup the [class]_permalink, e.g.
    my_model_permalink in your current site URLs to determine what url to use as
    the permalink. Think can be overridden using the 'url' parameter, or the
    additional decorator function (see decorators/__init__.py).
    
    The decorator function can also be used to maintain compatibility with the
    get_absolute_url function, as used by the admin system and various other
    Django pluggables.
    
    The filter will attempt to extract any parameters from the url, and replace
    them with the equivalent field. For example, in your relevant urls.py file:
    
        url(
            r'^read-article/(?P<id>\d+)_(?P<slug>[-\w]+).html',
            view=read_article, name='article_permalink'
        )
        
    When {{my_article|permalink}} is called in a template, the filter will try
    and resolve the 'article_permalink' URL, substituting in the id and slug 
    fields where the parameters are given:
    
        The Article model has additional slug unique field (along with default
        Django auto id field).
        
        Article instance has: id = 1, slug = 'example-article'
        
    The filter would take the article_permalink URL, and attempt to substitute
    any parameters specified within the url with their equivalent field value,
    giving in this case:
        
        read-article/1_example-article.html

    If the article_permalink (or specified) url is not defined, or any 
    parameters cannot be resolved, a TemplateError will be raised
    '''
          
    if not url:
            url = "%s_permalink" % object.__class__.__name__.lower()

    try:
            v = get_callable(url)
            l = get_resolver(None).reverse_dict.getlist(url)
            u = None

            if not l:
                    raise Exception("Cannot resolve url '%s'" % url)
            for possibility, pattern in l:
                    for result, params in possibility:
                            try:
                                    p = {}
                                    for par in params:
                                            p[par] = getattr(object, par)
                                    u = reverse(url, kwargs=p)
                            except:
                                    pass

            if not u:
                    raise TemplateSyntaxError(
                            "Could not resolve a valid url for '%s' and object '%s'" % (
                                    url, object.__class__.__name__
                            )
                    )
    except Exception, ex:
            raise TemplateSyntaxError(
                    "URL named '%s' must be defined " % url +
                    "in your urls.py file to use permalink filter (%s)" % ex
            )

    return u

register.filter('permalink', permalink)
