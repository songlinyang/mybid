from django.db import models

# Create your models here.

#产品类型表
class Product(models.Model):
    """产品表"""

    product_match_type = models.TextField("产品类型",max_length=20)

    def __str__(self):
        return self.product_match_type




#用户表
class Invest(models.Model):

    """用户表"""
    user_name = models.TextField("账号",max_length=15)
    pass_word = models.TextField("密码",max_length=15)
    pjb_url = models.TextField("出借平台地址", max_length=50)

    """产品购买表"""
    plan_id = models.IntegerField("出借产品")
    invest_amount = models.BigIntegerField("出借金额")
    invest_total = models.IntegerField("出借次数")
    invest_status = models.BooleanField("出借状态", default=False)
    order_status = models.BooleanField("锁定状态",default=False)
    err_msg = models.TextField("错误日志", max_length=255, default="正常")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Match(models.Model):
    """匹配表"""
    User = models.ForeignKey(Invest, on_delete=models.Case)
    Type = models.ForeignKey(Product, on_delete=models.Case)

    def __str__(self):
        return str(self.User)



#产品购买表
class Assign(models.Model):
    """
    
    """
