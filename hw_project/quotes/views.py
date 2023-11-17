from django.core.paginator import Paginator
from .models import Author
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote, Tag
from .forms import QuoteForm
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# def main(request, page=1):
#     db = get_mongo_db()
#     quotes = db.quotes.find()
#     per_page = 51
#     paginator = Paginator(list(quotes), per_page)
#     quotes_on_page = paginator.page(page)
#     return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def main(request, page=1):
    quotes = Quote.objects.all()
    tags = Tag.objects.annotate(quote_count=Count('quote')).order_by('-quote_count')
    top_tags = tags[:10]
    per_page = 15
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'tags': top_tags})


@login_required
def add_quote(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)

        if form.is_valid():
            try:
                list_tags = request.POST.getlist('tags')
                new_quote = form.save()

                choice_tags = Tag.objects.filter(name__in=list_tags)
                for tag in choice_tags.iterator():
                    new_quote.tags.add(tag)

                return redirect(to="quotes:root")
            except ValueError as err:
                return render(request, 'quotes/add_quote.html', {"tags": tags, 'form': QuoteForm(), 'error': err})

    return render(request, 'quotes/add_quote.html', {"tags": tags, 'form': QuoteForm()})



def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    quotes_by_author = author.quote_set.all()

    context = {'author': author, 'quotes_by_author': quotes_by_author}
    return render(request, 'quotes/author_detail.html', context)

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    context = {'tag': tag, 'quotes_10':quotes}
    return render(request, 'quotes/tag_detail.html', context)

@login_required
def quote_detail(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    return render(request, 'quotes/quote_detail.html', {'quote': quote})


@login_required
def delete_quote(request, quote_id):
    quote = Quote.objects.get(pk= quote_id)
    quote.delete()
    messages.success(request, 'Quote successfully deleted!')
    return render(request, 'quotes/quote_edit_deleted.html')

@login_required
def edit_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)

    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quote successfully edited!')
            return render(request, 'quotes/quote_edit_deleted.html')
    else:
        form = QuoteForm(instance=quote)

    return render(request, 'quotes/quote_edit.html', {'form': form, 'quote': quote})