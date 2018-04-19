from django import template
from django.urls import reverse_lazy

register = template.Library()

def constructKwargs(**kwargs):
    obj = kwargs.pop('object')
    usr = kwargs.pop('user')
    args = kwargs.pop('args')

    newkw = {}
    for k, v in args.items():
        subobj = obj
        for i in v:
            subobj = getattr(subobj, i)
        newkw.update({k: subobj})
    return newkw

@register.inclusion_tag('scrud/list_options.html', takes_context=True)
def listoptionmaker(context, tt):
    item = {}
    options = []
    for key, opt in context['urlOptions'].items():
        if "priority" in opt:
            item = {'btnClass':opt['btnClass'], 'url': reverse_lazy(opt['url'], kwargs=constructKwargs(**{'object': tt, 'user':'oi' , 'args': opt['args']})), 'label': key.title()}
        else:
            options.append({'btnClass':opt['btnClass'], 'url': reverse_lazy(opt['url'], kwargs={'pk': tt.id}), 'label': key.title()})

    return {'item': item, 'options': options}

@register.inclusion_tag('scrud/list_options.html')
def sublistoptionmaker(obj, urlOptions):
    item = {}
    options = []
    for key, opt in urlOptions.items():
        if "priority" in opt:
            item = {'btnClass':opt['btnClass'], 'url': reverse_lazy(opt['url'], kwargs=constructKwargs(**{'object': obj, 'user':'oi' , 'args': opt['args']})), 'label': key.title()}
        else:
            options.append({'btnClass':opt['btnClass'], 'url': reverse_lazy(opt['url'], kwargs={'pk': obj.id}), 'label': key})

    return {'item': item, 'options': options}

@register.inclusion_tag('scrud/detail_options.html', takes_context=True)
def detailoptionmaker(context, tt):
    options = []
    for key, opt in context['urlOptions'].items():
        options.append({'btnClass':opt['btnClass'], 'url': reverse_lazy(opt['url'], kwargs=constructKwargs(**{'object': tt, 'user':'oi' , 'args': opt['args']})), 'label': key.title()})

    return {'options': options}

@register.inclusion_tag('scrud/header_options.html', takes_context=True)
def boxheader(context, url):
    options = {'url': reverse_lazy(url['url'], kwargs=constructKwargs(**{'object': context['object'], 'user':'oi', 'args': url['args']}))}

    return {'urlOption': options}
