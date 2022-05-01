from django import forms
from .models import Topic,Reply

#フォームクラスを作る
class TopicForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "category","comment","image","user" ]

#モデルを使用したフォームクラスで検索してしまうと、モデルフィールドの仕様まで引き継ぐ。
#例えば、max_length=10の場合、10文字までしか検索のキーワードに指定できない状態になってしまう(10文字以上はバリデーションNG)
#だから、あえてモデルを使用しないフォームクラスを作り、文字数の制限等を引き継がないようにする
class SearchForm(forms.Form):
    search  = forms.CharField()


#選択されたカテゴリが実在するかのチェックも行うため、モデルを使用したフォームクラスでカテゴリ検索を行う
class TopicCategoryForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "category" ]

class ReplyForm(forms.ModelForm):
    class Meta:
        model   = Reply
        fields  = [ "topic","comment","user","secret" ]
