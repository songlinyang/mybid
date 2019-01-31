from django.contrib import admin
from invest_app.models import Invest,Product,Match
from django import forms



class InvestAdmin(admin.ModelAdmin):
    search_fields = ['user_name']
    list_display = ('id','user_name', 'pass_word','pjb_url','plan_id','invest_amount','invest_total','invest_status','order_status','err_msg')
    list_filter = ('invest_status',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_match_type',)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id','User','Type',)

admin.site.register(Invest,InvestAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Match,MatchAdmin)
    # user_name = models.TextField("账号", max_length=15)
    # pass_word = models.TextField("密码", max_length=15)
    # pjb_url = models.TextField("出借平台地址", max_length=50)
    #
    # """产品购买表"""
    # plan_id = models.IntegerField("出借产品")
    # invest_amount = models.BigIntegerField("出借金额")
    # invest_total = models.IntegerField("出借次数")
    # invest_status = models.BooleanField("出借状态", default=False)
    # product_type = models.IntegerField("产品类型")  # 3.0 或 2.0 或 票票贷
    # err_msg = models.TextField("错误日志", max_length=255, default="正常")
    # create_time = models.DateTimeField(auto_now_add=True)