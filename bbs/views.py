from django.shortcuts import render,redirect
from django.views import View

#ビューにアクセスしてきた時、ユーザーが認証済みであるかチェックする(認証済みであればそのまま実行、未認証であればログインページへリダイレクトする)
from django.contrib.auth.mixins import LoginRequiredMixin

#ここでmodels.pyのモデルクラスをimportする
from .models import Topic,Category,Reply
from .forms import TopicForm,ReplyForm,TopicCategoryForm,SearchForm

from django.db.models import Q
from django.core.paginator import Paginator


#多重継承。基本のビュークラスに認証状態のチェック機能を追加する
#class IndexView(LoginRequiredMixin,View):

class IndexView(View):

    def get(self, request, *args, **kwargs):

        #DBへの読み込み処理(filterで絞り込み、order_byで並び替えができる)

        context = {}
        query   = Q()

        form = TopicCategoryForm(request.GET)

        #TODO:現状ではcategoryフィールドはnull=True,blank=Trueになっているので、そのままアクセスした場合はカテゴリ未指定のみ表示されてしまう。
        #TODO:models.pyにて、categoryを指定必須にするか、フォームクラスにてカテゴリの指定必須に書き換えるかの対策が必要
        if form.is_valid():
            cleaned = form.clean()
            query &= Q(category=cleaned["category"])


        form = SearchForm(request.GET)

        if form.is_valid():
            cleaned = form.clean()

            #["Django","","","","教科書"]
            #["Django","教科書"]
            raw_words   = cleaned["search"].replace("　"," ").split(" ")
            #リストの内包表記で、空文字列があれば除去している。(OR検索の時に空文字列があると全件表示されてしまう)
            words       = [ w for w in raw_words if w != "" ]
            #↑と↓は等価
            """
            words = []
            for w in raw_words:
                if w != "":
                    words.append(w)
            """
            for w in words:
                query &= Q(comment__contains=w)


        #TODO:ページネーションを実装する時、order_byがないと警告が出る点に注意！！
        topics      = Topic.objects.filter(query).order_by("-dt")
        paginator   = Paginator(topics,2)

        if "page" in request.GET:
            context["topics"]   = paginator.get_page(request.GET["page"])
        else:
            context["topics"]   = paginator.get_page(1)


        #実行しているSQLの確認
        #print(Topic.objects.filter(query).query)

        context["categories"] = Category.objects.all()

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        #未認証であれば投稿を拒否する
        if not request.user.is_authenticated:
            print("未認証です")
            #return redirect("bbs:index")
            return redirect("account_login") #リダイレクト先はallauthのログインページへ

        print("POSTメソッド")
        #requestオブジェクトは書き換え不可能
        #request.POST["user"] = request.user.id

        #書き換え不可能なので.copy()を使ってコピーのオブジェクトを作る。
        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        #受け取ったデータを引数にして、フォームクラスのオブジェクトを作る
        #TODO:送信されたファイルもセットでバリデーションをする
        #form = TopicForm(request.POST,request.FILES)
        form = TopicForm(copied, request.FILES)

        #バリデーションルールに則っていればTrue、違反していればFalseを返す
        if form.is_valid():
            print("バリデーションOK")
            #DBへ書き込み
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        #POSTメソッドではレンダリングはしてはいけない
        #return render(request, "bbs/index.html")

        #POSTメソッドでは処理の終了後、リダイレクト(別ページに転送)を行う
        return redirect("bbs:index")

index   = IndexView.as_view()


class SingleView(View):
    def get(self, request, pk, *args, **kwargs):
        print(pk)
        context = {}
        context["topic"]    = Topic.objects.filter(id=pk).first()
        context["replies"]  = Reply.objects.filter(topic=pk)
        return render(request,"bbs/single.html",context)

    def post(self, request, pk, *args, **kwargs):
        copied          = request.POST.copy()
        copied["user"]  = request.user.id
        copied["topic"] = pk

        form = ReplyForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect("bbs:single",pk)

single  = SingleView.as_view()

