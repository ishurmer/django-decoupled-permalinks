def auto_permalink(f):
    '''Decorator function to maintain compatibility with that
    horrendous get_absolute_url function, used in conjunction with the
    permalink filter (see templates/filters.py)
    
    f is a function returning an optional url name if you wish to override
    the default [class]_permalink

    e.g.

        @auto_permalink
                def get_absolute_url(self):
                    pass                        

    '''
    from templates.filters import permalink as p
    def i(*args, **kwargs):
        v = f(*args, **kwargs)
        return p(args[0], v)

    return i
