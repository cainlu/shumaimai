#coding=utf-8

import datetime

from django.core.signals import * 
from django.db.models.signals import *
from django.dispatch import receiver
from django.conf import settings
from django.contrib.sites import models as site_models

import models as book_models
from models import *
from utils import *

@receiver(post_syncdb, sender=site_models)
def init_site(sender, **kwargs):
    site = site_models.Site.objects.get_current() 
    if settings.SITE_DOMAIN:
        site.domain = settings.SITE_DOMAIN
    else:
        site.domain = 'localhost:8000'
    if settings.SITE_NAME:
        site.name = settings.SITE_NAME
    else:
        site.name = 'Shumaimai'
    site.save()

#@receiver(post_syncdb, sender=book_models)
#def school_course_init(sender, **kwargs):
#    School.objects.all().delete()
#    #c1, created = Course.objects.get_or_create(name="高等数学")
#    #c2, created = Course.objects.get_or_create(name="计算机")
#    #c3, created = Course.objects.get_or_create(name="物理")
#    s1 = School.objects.create(id=1, name="上海海洋大学", region="CN-31") 
#    #s2, created = School.objects.get_or_create(name="北京大学", region="CN-11") 
#    #s2.course.add(c1, c2, c3)
#    s3 = School.objects.get_or_create(id=2, name="上海海事大学", region="CN-31") 
#
#@receiver(post_syncdb, sender=book_models)
#def taxonomy_book_init(sender, **kwargs):
#
#    # init taxonomy
#    Taxonomy.objects.all().delete()
#
#    # level 1
#    t_1_textbook = Taxonomy.objects.create(id=1, name=u"二手教材", parent=None, weight=5)
#    t_1_novel = Taxonomy.objects.create(id=2, name=u"就爱阅读", parent=None, weight=3)
#    t_1_more = Taxonomy.objects.create(id=3, name=u"更多发现", parent=None, weight=3)
#    
#    # level 2
#    Taxonomy.objects.create(id=4, name=u"航运与交通运输", parent=t_1_textbook, weight=t_1_textbook.weight)
#    Taxonomy.objects.create(id=5, name=u"经济金融", parent=t_1_textbook, weight=t_1_textbook.weight)
#    Taxonomy.objects.create(id=6, name=u"工商管理", parent=t_1_textbook, weight=t_1_textbook.weight)
#    Taxonomy.objects.create(id=7, name=u"艺术设计", parent=t_1_textbook, weight=t_1_textbook.weight)
#    Taxonomy.objects.create(id=8, name=u"法律、语言、人文社科", parent=t_1_textbook, weight=t_1_textbook.weight)
#    Taxonomy.objects.create(id=9, name=u"计算机与信息科学", parent=t_1_textbook, weight=t_1_textbook.weight)
#    Taxonomy.objects.create(id=10, name=u"自然科学", parent=t_1_textbook, weight=t_1_textbook.weight)
#    Taxonomy.objects.create(id=11, name=u"工程机械", parent=t_1_textbook, weight=t_1_textbook.weight)
#    Taxonomy.objects.create(id=12, name=u"考试教辅", parent=t_1_textbook, weight=t_1_textbook.weight)
#
#
#    t_2_novel_1 = Taxonomy.objects.create(id=13, name=u"自我管理",  parent=t_1_novel, weight=t_1_novel.weight)   
#    t_2_novel_2 = Taxonomy.objects.create(id=14, name=u"散文小说",  parent=t_1_novel, weight=t_1_novel.weight)   
#    t_2_novel_3 = Taxonomy.objects.create(id=15, name=u"趣味科学",  parent=t_1_novel, weight=t_1_novel.weight)   
#    t_2_novel_4 = Taxonomy.objects.create(id=16, name=u"人物传记",  parent=t_1_novel, weight=t_1_novel.weight)   
#    t_2_novel_5 = Taxonomy.objects.create(id=17, name=u"阅读经典",  parent=t_1_novel, weight=t_1_novel.weight)   
#    t_2_novel_6 = Taxonomy.objects.create(id=18, name=u"畅销图书",  parent=t_1_novel, weight=t_1_novel.weight)   
#    t_2_novel_7 = Taxonomy.objects.create(id=19, name=u"吃喝玩乐",  parent=t_1_novel, weight=t_1_novel.weight)   
#    
#    ## init book
#    #Book.objects.all().delete()
#
#    #book1, created = Book.objects.get_or_create(
#    #        name = u"孔雀の道",
#    #        author = u"陈舜臣",
#    #        translator = u"袁斌",
#    #        language = 'ja',
#    #        publication_date = datetime.datetime(2012, 9, 1),
#    #        price_ori = 29.8,
#    #        price_old = 15,
#    #        number = 1,
#    #        status = 1,
#    #        isbn = u"9787550208407",
#    #        press = u"北京联合出版公司",
#    #        description = u"""
#    #一个火球般炽热的女人，一段夷所思的跨国婚姻，一段剪不断理还乱的恩怨情仇……
#    #    时隔十三年，英日混血儿罗丝带着对日本的憧憬重返母亲国。不料刚到神户，住在隔壁的法国老妇人便惨遭杀害，而死者正是已故父母的旧相识。随着调查的深入，一连串被岁月湮没的杀人案逐渐浮出水面。间谍、勒索、暗杀、大火……所有的矛头都指向父亲，却无法解释眼前这桩惨案。凶手到底是谁？动机何在？与母亲的死又有何关联？当谜底揭晓的那一刻，生命是否依然能如孔雀开屏一般华丽炫耀眼？
#    #        """,
#    #    )
#    #if created:
#    #    book1.add_taxonomy(t_2_novel_1)
#    #book2, created = Book.objects.get_or_create(
#    #        name = u"成为和平饭店",
#    #        author = u"陈丹燕",
#    #        press = u"上海文艺出版社",
#    #        publication_date = datetime.datetime(2012, 8, 1),
#    #        price_ori = 30,
#    #        price_old = 15,
#    #        isbn = u"9787532145652",
#    #        language = 'en',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        《成为和平饭店》，陈丹燕上海系列故事最新作品。全书以一栋建筑为主线，讲述了和平饭店这一富有象征意义、遍布历史遗痕的上海纪念碑式建筑的前世今生。作者以非虚构小说的方式介入历史，以细节和史实为经纬，交织人物与故事，构成一部亦真亦幻的建筑生命史。 成为“和平饭店”，成为上海的历史见证——陈丹燕为我们展现了一座建筑在时光穿梭中往复飘荡的风景，和一座城市在风云激荡中缄默却不息的记忆……
#    #        """,
#    #    )
#    #if created:
#    #    book2.add_taxonomy(t_2_novel_2)
#    #book3, created = Book.objects.get_or_create(
#    #        name = u"减肥这正经事儿",
#    #        author = u"粽", press = u"光明日报出版社",
#    #        publication_date = datetime.datetime(2012, 8, 1),
#    #        price_ori = 25,
#    #        price_old = 12.5,
#    #        isbn = "9787511228550",
#    #        language = 'zh',
#    #        number = 1,
#    #        status = 1,
#    #        description = """
#    #        这是一本以减肥为主题的漫画书。书里面的女孩都是一直在努力减肥，期许美好的生活的小胖子。而本书正是讲述了她们漫漫减肥生涯中发生的各种趣事囧事糗事。姑娘们乐观、坚持的心态，直击读者笑点，胖瘦不重要，做自己最好。 
#    #        """,
#    #    )
#    #if created:
#    #    book3.add_taxonomy(t_2_novel_3)
#    #book4, created = Book.objects.get_or_create(
#    #        name = u"请勿再次丢弃尸体",
#    #        author = u"东川笃哉",
#    #        press = u"新星出版社",
#    #        publication_date = datetime.datetime(2012, 8, 30),
#    #        price_ori = 26,
#    #        price_old = 20,
#    #        isbn = "9787513306263",
#    #        language = 'zh',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        青春漂亮可爱善良的女大学生有坂春佳一时糊涂在家里杀了个陌生女子，慌了神的她只得打电话向废物姐姐求助。习惯了在妹妹家蹭吃蹭喝蹭住的有坂香织发誓，这次一定要挽回作为姐姐的面子！
#    #        　　可要神不知鬼不觉地弃尸，何其容易！被杀的女人又是怎么闯入妹妹家的？然而此时香织来不及多想，她更在意的是——总跟着我的这个神经病侦探到底是怎么回事啊？！
#    #        　　对不起，这里不能弃尸哦~ 
#    #        """,
#    #    )
#    #if created:
#    #    book4.add_taxonomy(t_2_novel_3)
#    #book5, created = Book.objects.get_or_create(
#    #        name = u"恐怖的人狼城·第四部：完结篇",
#    #        subtitle = u"嗜血者的挽歌",
#    #        author = u"二阶堂黎人",
#    #        press = u"新星出版社",
#    #        publication_date = datetime.datetime(2012, 8, 1),
#    #        price_ori = 33,
#    #        price_old = 12.4,
#    #        isbn = "9787513307062",
#    #        language = 'ja',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        美少女侦探二阶堂兰子终于踏进了传说中的人狼城——银狼城与青狼城隔崖相望，传说与现实在这里碰撞。面对着精心营造的巨大陷阱，面对着一件件奇迹似的不可能犯罪，面对着世人所难以想象的深度恶意，面对着几近无法战胜的对手，兰子要如何解开这个震惊世界的杀戮谜团…… 
#    #        """,
#    #    )
#    #if created:
#    #    book5.add_taxonomy(t_2_novel_3)
#    #book6, created = Book.objects.get_or_create(
#    #        name = u"死者的留言",
#    #        subtitle = u"古畑任三郎 2",
#    #        author = u"三谷幸喜",
#    #        translator = u"陆丽丹",
#    #        press = u"化学工业出版社",
#    #        publication_date = datetime.datetime(2012, 9, 1),
#    #        price_ori = 25.4,
#    #        price_old = 12.5,
#    #        isbn = "9787122144850",
#    #        language = 'fr',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        少女漫画家谋杀了自己的花心恋人。因为一张旧稿纸暴露了自己是凶手的真相。 
#    #        """,
#    #    )
#    #if created:
#    #    book6.add_taxonomy(t_2_novel_1)
#    #book7, created = Book.objects.get_or_create(
#    #        name = u"你迟到了许多年",
#    #        author = u"金陵雪",
#    #        press = u"中国华侨出版社",
#    #        publication_date = datetime.datetime(2012, 9, 1),
#    #        price_ori = 29.4,
#    #        price_old = 13,
#    #        isbn = "9787511313744",
#    #        language = 'ru',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        　　我要你知道，在这个世界上总有一个人是等着你的，
#    #        　　不管在什么时候，不管在什么地方，反正你知道，总有这么个人。
#    #        　　刻意封缄的旧时光里，他是一抹不经意的掠影，她是灼伤自己的星光，
#    #        　　曾被爱摧毁的心，如何于尘埃中开出花来？
#    #        　　《大爱晚成》后，金陵雪再献都市暖爱救赎
#    #        　　续写张爱玲、亦舒、张小娴笔下“百转千回”的爱！
#    #        　　一场注定汹涌的灵魂骚动。还记得最初让你痛哭的人吗？
#    #        　　未再、李李翔、云五、网易原创携千万读者感动推荐！
#    #        　　你来，永不太迟——致所有的“得不到”和“已失去”
#    #        　　………………………………………………………………
#    #        　　有多久没见你，以为你在哪里，原来你就住在我的梦里，陪伴着我的呼吸。
#    #        　　曾经人人都当她是玻璃罩里的玫瑰，
#    #        　　童话破灭了许多年，她竟似野草般活到今日。
#    #        　　爱，爱，爱……
#    #        　　这世间的爱于她而言，曾是阳光雨露、蛋糕蜜糖一样唾手可得的东西。
#    #        　　直到剧情瞬间坍塌，星光陨落。
#    #        　　他的出现，是她平静生活里的狂雷闪电。
#    #        　　梦中纠缠多年的无脸人被赋予五官，却愈加狰狞。
#    #        　　一个大信封，果断地断她生计，却又峰回路转，与她合演一场险象横生的戏。
#    #        　　她久无风浪的心，开始因一个约定而摆荡。
#    #        　　他是何时认出她，或许仍在试？
#    #        　　无脸人唇角竟漾出笑意，他向她伸出手，是梦境的接壤，抑或另一段故事的伊始？
#    #        　　好多好多年过去了，她都忘了，被那铺天盖地毫无道理的爱包围的感觉。
#    #        　　她曾经被宠坏，又跌至谷底。他年少动荡，早已忘却温暖的滋味。
#    #        　　终于，在迂回的迷藏中找到彼此，轻轻问一句：
#    #        　　咦，好像在哪里见过你？
#    #        　　就算世界无童话，如你信爱，废墟中亦能开出花来。　
#    #        """,
#    #    )
#    #if created:
#    #    book7.add_taxonomy(t_2_novel_1)
#    #book8, created = Book.objects.get_or_create(
#    #        name = u"陈春天",
#    #        subtitle = u"陈雪自传体三部曲之二",
#    #        author = u"陈雪",
#    #        press = u"新星出版社",
#    #        publication_date = datetime.datetime(2012, 4, 1),
#    #        price_ori = 28,
#    #        price_old = 13,
#    #        isbn = "9787513308045",
#    #        language = 'en',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        《陈春天》是陈雪继《桥上的孩子》之后的第二部自传体长篇小说，但着力点从“个人”转向了“家庭”，《陈春天》围绕两条主线展开：一条线索是主人公陈春天的家庭变故，包括父亲破产、母亲出走，全家人被故乡亲人邻里歧视与放逐，其间穿插陈春天在爱情中的多次自我放逐；另一条主线是陈春天的弟弟所经历的一场严重车祸。从急诊室、手术房、加护病房、普通病房到出院回“家”，陈春天一步步走近家人，走进他们的内心世界。终篇的一场家族丧礼则连接了两条线索，陈春天和弟弟妹妹一起回到家族中，达成了与家人的和解，最终完成了从“放逐”到“回归”的过程。 
#    #        """,
#    #    )
#    #if created:
#    #    book8.add_taxonomy(t_2_novel_1)
#    #book9, created = Book.objects.get_or_create(
#    #        name = u"云治",
#    #        subtitle = u"这些都是你给我的爱Ⅱ",
#    #        author = u"安东尼/echo",
#    #        press = u"长江文艺出版社,长江出版传媒",
#    #        publication_date = datetime.datetime(2012, 8, 10),
#    #        price_ori = 32.8,
#    #        price_old = 25,
#    #        isbn = "9787535457790",
#    #        language = 'fr',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        　　这些都是你给我的爱Ⅱ 云治
#    #        　　安东尼著 echo绘
#    #        　　2012年8月10日 温情上市
#    #        　　随书附赠安东尼+echo全彩印刷《They write,draw and travel》新西兰旅行随路本
#    #        　　爱 到底是什么样的 是什么形状 味道 温度 有没有颜色 要如何捕捉
#    #        　　它是否可以“光合作用” 犹如氧气般存在 让我们呼吸
#    #        　　还是简单的 就像第一次见面时你扬起嘴角 微笑着说的两个字 “你好”
#    #        　　类似这样的问题一次次地在我脑海中出现 但是所有给出的答案 又一次次被推翻
#    #        　　从《这些都是你给我的爱》到《云治》
#    #        　　从一个人踏上旅途 寻找开满鲜花的树 到带着一颗陶瓷红心 全世界漫无目的地流浪
#    #        　　——Echo&Anthony上 
#    #        """,
#    #    )
#    #if created:
#    #    book9.add_taxonomy(t_2_novel_2)
#    #book10, created = Book.objects.get_or_create(
#    #        name = u"再不相爱就软了",
#    #        author = u"彭浩翔",
#    #        press = u"百花洲文艺出版社",
#    #        publication_date = datetime.datetime(2012, 6, 2),
#    #        price_ori = 29.8,
#    #        price_old = 14,
#    #        isbn = "9787550001787",
#    #        language = 'zh',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        彭浩翔察人观事，泼墨经年，挥洒自在。这本杂文集选自彭浩翔颇受好评的港版杂文集《一种风流》和《坐牢切勿拾肥皂》，不仅辑录了作者2005年到2009年间为CUP，HIM，Pandaa等香港报刊杂志撰写的专栏，同时在该简体版中也另增录了作者新近的杂文创作。在本书中，彭浩翔细论感情琐事，畅谈电影制作，拉杂世事，游历文艺生活的方方面面。浸染于书中的，是作者体味身边人和事时的独到韵味。此次更邀请跨界摄影大师郑中基为书中散文拍摄相配照片。 
#    #        """,
#    #    )
#    #if created:
#    #    book10.add_taxonomy(t_2_novel_2)
#    #book11, created = Book.objects.get_or_create(
#    #        name = u"我不要你死于一事无成",
#    #        subtitle = u"给女儿的17封告别信",
#    #        author = u"[阿富汗] 法齐娅·库菲",
#    #        translator = u"章忠建",
#    #        press = u"中信出版社",
#    #        publication_date = datetime.datetime(2012, 6, 1),
#    #        price_ori = 28,
#    #        price_old = 28,
#    #        isbn = "9787508633220",
#    #        language = 'zh',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        　　法齐娅•库菲，阿富汗唯一一位女性国会议长，自童年开始便亲眼目睹阿富汗人民的苦难与悲惨，立誓投身政治，面对质疑，诽谤，不公正的政治环境，一次次的暗杀与迫害，她始终坚定地与所有反对力量抗争，也幸运地躲过了一次次死亡的威胁。
#    #        　　她有一个 “我永远不会站在你和你的祖国之间”的丈夫和一段凄美至极的爱情。她代表阿富汗最贫穷地区的利益，代表正义的力量，她每一次走出家门都是充满危险的未知旅程，都无法保证自己能否平安返回，于是她只能在每次出门前给最亲爱的两个女儿留下一封信：如果她不在了，女儿们要怎样面对生活。请不要悲伤，你们要从中汲取，犹存的力量。
#    #        　　尽管生命充满苦痛与辛酸，但这本书里的每一段悲痛的情节都能让人见到希望的阳光。信仰超越了死亡，岁月沉淀了从容，绽放出最夺目的光彩。
#    #        　　名人或者媒体评论：
#    #        　　她的人生是一次次劫难，可她在劫难后收获的是勇气。她的民族经历一遍遍暴虐，可她在断璧残垣中仍要寻找正义。这不只一本自传，也是从泪水和战火中淬炼出的至诚、至善的声音。
#    #        　　——《新周刊》主笔 蒋方舟
#    #        　　“自由地过你们想要的生活，实现你们所有的梦想。”本书中字里行间渗透出来的是母爱这种伟大的力量，包含了一个母亲的言传身教和对孩子的人生期望。库菲更是一个把最高的抱负献给国家，把最深的爱留给女儿的坚强不屈的传奇女性。
#    #        　　——《南方人物周刊》资深记者 薛芳
#    #        　　她的每一次活着，都是正义力量的又一次胜利。
#    #        　　——《三联生活周刊》编辑 贝小戎
#    #        　　面对困境，越挫越勇，这就是本书对这种生活的真实写照。《我不要你死于一事无成：给女儿的17封告别信》有时读来令人残忍，有时令人震惊，称其鼓舞人心一点儿不为过。读罢此书，好好感恩生活赋予你的如许机会吧。
#    #        　　——著名作家 安德里亚•布斯菲尔德
#    #        　　库菲亲历的故事引人入胜，读来令人身临其境……她巧妙地勾画出一个在文化传统和标准上都历经变革的阿富汗，并阐述其对女性产生的深远影响，其笔触之细腻，是关于阿富汗女性生活的一般报道所不可企及的。……这确实是一个鼓舞人心、勇敢大胆的故事。
#    #        　　——《穆斯林媒体观察》
#    #        　　《我不要你死于一事无成：给女儿的17封告别信》向读者展现了一个不该被我们忘记和忽视的世界。
#    #        　　——《明州星报》
#    #        　　作为阿富汗最直言不讳的民主运动激进分子之一，库菲亲身经历并勇敢地揭露了阿富汗在战乱年代，造成阿富汗许多无谓杀戮的根源。
#    #        　　——加拿大《环球邮报》　　 
#    #        """,
#    #    )
#    #if created:
#    #    book11.add_taxonomy(t_2_novel_1)
#    #book12, created = Book.objects.get_or_create(
#    #        name = u"偷影子的人",
#    #        author = u"马克·李维",
#    #        translator = u"段韵灵",
#    #        press = u"湖南文艺出版社",
#    #        publication_date = datetime.datetime(2012, 7, 1),
#    #        price_ori = 29.3,
#    #        price_old = 12,
#    #        isbn = "9787540455958",
#    #        language = 'en',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        《偷影子的人》内容简介：不知道姓氏的克蕾儿。这就是你在我生命里的角色，我童年时的小女孩，今日蜕变成了女人，一段青梅竹马的回忆，一个时间之神没有应允的愿望。一个老是受班上同学欺负的瘦弱小男孩，因为拥有一种特殊能力而强大：他能“偷别人的影子”，因而能看见他人心事，听见人们心中不愿意说出口的秘密。他开始成为需要帮助者的心灵伙伴，为每个偷来的影子找到点亮生命的小小光芒。某年灿烂的夏天，他在海边邂逅了一位又聋又哑的女孩。他该如何用自己的能力帮助她？他将如何信守与她共许的承诺？
#    #        """,
#    #    )
#    #if created:
#    #    book12.add_taxonomy(t_2_novel_1)
#    #book13, created = Book.objects.get_or_create(
#    #        name = u"给樱桃以性别",
#    #        author = u"(英)珍妮特·温特森",
#    #        translator = u"邹鹏",
#    #        press = u"新星出版社",
#    #        publication_date = datetime.datetime(2012, 7, 10),
#    #        price_ori = 25,
#    #        price_old = 11,
#    #        isbn = "9787513306836",
#    #        language = 'ru',
#    #        number = 1,
#    #        status = 1,
#    #        description = u"""
#    #        《橘子不是唯一的水果》姐妹篇
#    #        　　1990年E.M.福斯特获奖作品
#    #        　　2009年《泰晤士报》“六十年六十佳图书”入选作品
#    #        　　米兰•昆德拉的哲学架构+卡尔维诺的优雅叙事+《天方夜谭》的故事
#    #        　　张悦然诚挚推荐 《鲤》杂志参与策划
#    #        　　17世纪，英国查尔斯二世时期，在臭气熏天的泰晤士河旁边生活着一个女巨人。她丑陋、孤独，只和很多狗生活在一起。有一天，她在河岸边看到了一个弃儿，便将他收养，并给他一条河流的名字，叫约旦。约旦和他的母亲生活在一起，一直遇到了国王的园艺师。园艺师将他们带到了温布尔顿，让约旦学习园艺。后来，约旦追随园艺师前往百慕大群岛，一个据说离天堂最近的地方，一路上遇到了很多奇怪的人和事情：十二个跳舞的公主，每个公主都在讲述着她与其丈夫的故事；遇到一个视爱为瘟疫的村子，因为爱，所有的人都死去，只剩下一个僧侣与妓女。与此同时，约旦的母亲在保皇党的鼓动下，对杀死国王的清教徒进行疯狂的复仇……
#    #        　　《给樱桃以性别》将历史、童话故事 和元小说熔合进了一种水果里，有着回味无穷、令人惊艳的味道。
#    #        　　——《纽约时报》
#    #        　　《给樱桃以性别》是一部以卡尔维诺的优雅口吻讲述、米兰•昆德拉的哲学形式编排的《天方夜谭》。
#    #        　　——《旧金山纪事报》
#    #        　　温特森是超级文字魔术师。持续阅读那些难以置信的故事时，她让我们相信，想象的力量可以改变我们感知的方式，从而使我们的生活变得鲜活。
#    #        　　——《英国独立报》
#    #        　　那些喜爱气质独特、行文优美的小说的读者都会愿意阅读温特森写下的任何篇章。
#    #        　　——《华盛顿邮报》　　 
#    #        """,
#    #    )
#    #if created:
#    #    book13.add_taxonomy(t_2_novel_3)
#



