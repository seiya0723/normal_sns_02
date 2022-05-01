from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):

    name    = models.CharField(verbose_name="カテゴリ名",max_length=20)

    #category検索時、requestオブジェクト内の値とidの型が不一致でselectedされないので、str型を返すメソッドで判定する
    def str_id(self):
        return str(self.id)

    def __str__(self):
        return self.name



class Topic(models.Model):

    category    = models.ForeignKey(Category,verbose_name="カテゴリ",on_delete=models.CASCADE)
    comment     = models.CharField(verbose_name="コメント",max_length=2000)
    dt          = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)

    image       = models.ImageField(verbose_name="画像",upload_to="bbs/topic/image/",null=True,blank=True)
    user        = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE, null=True,blank=True)


    def reply_amount(self):
        return Reply.objects.filter(topic=self.id).count()

    def __str__(self):
        return self.comment


class Reply(models.Model):

    topic   = models.ForeignKey(Topic,verbose_name="リプライ対象のトピック",on_delete=models.CASCADE)
    comment = models.CharField(verbose_name="コメント",max_length=2000)
    user    = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE, null=True,blank=True)

    secret  = models.BooleanField(verbose_name="投稿者にのみ表示させる",default=False)


    def __str__(self):
        return self.comment
