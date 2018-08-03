from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from article.models import Article,Comment
from article.forms import ArticleForm
from django.db.models.query_utils import Q
# Create your views here.
def article(request):
    '''
    Render the article page
    '''
#     articles = {}
#     for article in Article.objects.all():
#         articles.update({article:Comment.objects.filter(article=article)})
#     context = {'articles':articles}
    articles = Article.objects.all()
    comments = Comment.objects.all()
    context = {'articles':articles, 'comments':comments}
    
    return render(request, 'article/article.html', context)


def articleCreate(request):
    '''
    Create a new article instance
        1. If method is GET, render an empty form
        2. If method is POST, perform form validation and display error messages if the form is invalid
        3. Save the form to the model and redirect the user to the article page
    '''
    template = 'article/articleCreateUpdate.html'
    if request.method == 'GET':
        return render(request, template, {'articleForm':ArticleForm()})
    
    # POST
    articleForm = ArticleForm(request.POST)
    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm})
    articleForm.save()
    messages.success(request, '文章已新增')
    return redirect('article:article')

def articleRead(request, articleId):
    '''
    Read an article
        1. Get the "article" instance using "articleId"; redirect to the 404 page if not found
        2. Render the articleRead template with the article instance and its
           associated comments
    '''
    article = get_object_or_404(Article, id=articleId)
    context = {
        'article': article,
        'comments': Comment.objects.filter(article=article)
    }
    return render(request, 'article/articleRead.html', context)

def articleUpdate(request, articleId):
    '''
    Update the article instance:
        1. Get the article to update; redirect to 404 if not found
        2. Render a bound form if the method is GET
        3. If the form is valid, save it to the model, otherwise render a
           bound form with error messages
    '''
    article = get_object_or_404(Article, id=articleId)
    template = 'article/articleCreateUpdate.html'
    if request.method == 'GET':
        articleForm = ArticleForm(instance=article)
        return render(request, template, {'articleForm':articleForm})
    
    #POST
    articleForm = ArticleForm(request.POST, instance=article)
    if not articleForm.is_valid():
        return render(request, template, {"articleForm":articleForm})
    articleForm.save()
    messages.success(request, '文章已修改')
    return redirect('article:articleRead', articleId=articleId)


def articleDelete(request, articleId):
    '''
    Delete the article instance:
        1. Render the article page if the method is GET
        2. Get the article to delete; redirect to 404 if not found
    '''
    if request.method == 'GET':
        return article(request)
    #POST
    article = get_object_or_404(Article, id=articleId)
    article.delete()
    messages.success(request, '文章已刪除')
    return redirect('article:article')


def articleSearch(request):
    '''
    Search for articles:
        1. Get the "searchTerm" from the HTML page
        2. Use "searchTerm" for filtering
    '''
    searchTerm = request.GET.get('searchTerm')
    articles = Article.objects.filter(Q(title__icontains=searchTerm)|Q(content__icontains=searchTerm))
    context = {'articles':articles, 'searchTerm':searchTerm}
    return render(request, 'article/articleSearch.html', context)
