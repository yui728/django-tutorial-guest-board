from django.core.paginator import (
    Paginator, # ページネーター本体
    EmptyPage, # 指定したページ番号が範囲外の場合に表示するページ
    PageNotAnInteger # 指定したページ番号が数値以外の場合に発生する例外

)
from django.shortcuts import ( 
    render,
    redirect
)
from django.contrib import messages
from .models import Posting
from .forms import PostingForm

def _get_page(list_, page_no, count=5):
    """ページネーターを使い、表示するページ情報を取得する"""
    paginator = Paginator(list_, count)
    try:
        page = paginator.page(page_no)
    except (EmptyPage, PageNotAnInteger):
        # page_noが指定されていない場合、数値でない場合、範囲外の場合は
        # 先頭のページを表示する
        page = paginator.page(1)
    return page

def index(request):
    """表示・投稿を処理する"""
    # ModelFormもFormも処理するイミングは同じ
    form = PostingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '投稿を受け付けました。')
            return redirect('guestboard:index')
        else :
            messages.error(request, '入力内容に誤りがあります。')
    page = _get_page(
        Posting.objects.order_by('-id'),
        request.GET.get('page')
    )
    context = {
        'form': form,
        'page': page
    }
    return render(request, 'guestboard/index.html', context)
