from django.contrib import admin
from .models import Topic,Category

#管理サイトでTopicを読み書き編集削除できるように登録する
admin.site.register(Topic)
admin.site.register(Category)

