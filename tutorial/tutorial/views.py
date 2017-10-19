from docutils.core import publish_parts
import re

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .models import Page, Sentence

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")



@view_config(context='.models.Wiki')
def view_wiki(context, request):
    print('view_wiki ', context)
    return HTTPFound(location=request.resource_url(context, 'FrontPage'))


@view_config(context='.models.Page', renderer='templates/view.pt')
def view_page(context, request):
    wiki = context.__parent__
    print('view_page ', context)
    def check(match):
        word = match.group(1)
        if word in wiki:
            page = wiki[word]
            view_url = request.resource_url(page)
            return '<a href="%s">%s</a>' % (view_url, word)
        else:
            add_url = request.application_url + '/add_page/' + word
            return '<a href="%s">%s</a>' % (add_url, word)

    content = publish_parts(context.data, writer_name='html')['html_body']
    content = wikiwords.sub(check, content)
    edit_url = request.resource_url(context, 'edit_page')
    return dict(page=context, content=content, edit_url=edit_url)

@view_config(name='add_page', context='.models.Wiki', renderer='templates/edit.pt')
def add_page(context, request):
    print('add page')
    pagename = request.subpath[0]
    if 'form.submitted' in request.params:
        body = request.params['body']
        page = Page(body)
        page.__name__ = pagename
        page.__parent__ = context
        context[pagename] = page
        return HTTPFound(location=request.resource_url(page))
    save_url = request.resource_url(context, 'add_page', pagename)
    page = Page('')
    page.__name__ = pagename
    page.__parent__ = context
    return dict(page=page, save_url=save_url)

@view_config(name='edit_page', context='.models.Page', renderer='templates/edit.pt')
def edit_page(context, request):
    if 'form.submitted' in request.params:
        context.data = request.params['body']
        return HTTPFound(location=request.resource_url(context))

    return dict(page=context, save_url=request.resource_url(context, 'edit_page'))

@view_config(name='sentence', context='.models.Page')
def sentence(context, request):
    print('view page ', context)
    return HTTPFound(location=request.resource_url(context, 'sentence', request.subpath[0]))


@view_config(context=".models.Sentence", renderer="templates/view_sentence.pt")
def view_sentence(context, request):
    wiki = context.__parent__.__parent__
    page = context.__parent__

    print('view_sentence')

    def check(match):
        word = match.group(1)
        if word in page:
            sentence = page[word]
            view_url = request.resource_url(sentence)
            return '<a href="%s">%s</a>' % (view_url, word)
        else:
            add_url = request.application_url + '/add_sentence/' + word
            return '<a href="%s">%s</a>' % (add_url, word)

    content = publish_parts(context.data, writer_name='html')['html_body']
    content = wikiwords.sub(check, content)
    edit_url = request.resource_url(context, 'edit_sentence')
    return dict(sentence=context, content=content, edit_url=edit_url)

@view_config(name='add_sentence', context='.models.Page', renderer='templates/edit_sentence.pt')
def add_sentence(context, request):
    print('add sentence ', context)
    sentencename = request.subpath[0]
    if 'form.submitted' in request.params:
        body = request.params['body']
        sentence = Sentence(body)
        sentence.__name__ = sentencename
        sentence.__parent__ = context
        context.tree[sentencename] = sentence
        return HTTPFound(location=request.resource_url(sentence))
    save_url = request.resource_url(context, 'add_sentence', sentencename)
    sentence = Sentence('')
    sentence.__name__ = sentencename
    sentence.__parent__ = context
    return dict(sentence=sentence, save_url=save_url)

@view_config(name='edit_sentence', context='.models.Sentence', renderer='templates/edit_sentence.pt')
def edit_sentence(context, request):
    if 'form.submitted' in request.params:
        context.data = request.params['body']
        return HTTPFound(location=request.resource_url(context))

    return dict(sentence=context, save_url=request.resource_url(context, 'edit_sentence'))