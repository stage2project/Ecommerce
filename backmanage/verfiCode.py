import os
from io import BytesIO

from PIL import ImageFont,ImageDraw,Image
from random import randint

# 验证码
class VerfiCode:
    def __init__(self,width=80,height=35,size=4):
        """
        构造
        :param width: 图片宽度
        :param height: 图片高度
        :param size: 验证码字符个数
        """
        self.width = width
        self.height = height
        self.size = size

    @property
    def code(self):
        return self.__code

    def output(self):
        # 1 生成画布和画笔
        self.im = Image.new('RGB',(self.width,self.height),'white')
        self.pen = ImageDraw.Draw(self.im)

        # 2.生成验证码字符串
        self.__code = self.generate_string()

        # 3.画验证码字符
        self.__draw_string()

        # 4. 画干扰点
        self.__draw_point()
        # 5 画干扰线
        self.__draw_line()
        # 6 保存
        # self.im.save('vc.jpg')
        buf = BytesIO()
        self.im.save(buf,'jpeg')
        res = buf.getvalue()
        buf.close()
        return  res

    def __draw_line(self):
        for i in range(6):
            x1 = randint(1,self.width-1)
            x2 = randint(1,self.width-1)
            y1 = randint(1,self.height-1)
            y2 = randint(1,self.height-1)
            self.pen.line([(x1,y1),(x2,y2)],fill=self.__rand_color(30,150),width=2)

    def __draw_point(self):
        for i in range(200):
            x = randint(1,self.width-1)
            y = randint(1,self.height-1)
            self.pen.point((x,y),fill=self.__rand_color(60,120))

    def __rand_color(self,low,high):
        return randint(low,high),randint(low,high),randint(low,high)

    def __draw_string(self):
        root =  os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        path = os.path.join(root,'static/backmanage/font/fonts/SIMLI.TTF')
        myFont = ImageFont.truetype(path, size=20, encoding='utf-8')
        width = (self.width - 20) / self.size  #每个字符的宽度

        for i in range(self.size):
            ch = self.__code[i]
            x = 15 + i * width
            y = randint(0,10)
            self.pen.text((x,y),ch,fill=self.__rand_color(10,100),font=myFont)

    def generate_string(self):
        return ''.join([str(randint(0,9)) for i in range(self.size)])

vc = VerfiCode()
vc.output()
