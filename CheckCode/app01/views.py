#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response,HttpResponse
from app01.Helper import Checkcode
import StringIO

'''
python3 版本StringIO
另一个列子是看来来并不怎么优雅的StringIO类，在Python2中，纯Python版本是StringIO模块，
意味着访问的时候是通过StringIO.StringIO，同样还有一个更为快速的C语言版本，位于cStringIO.StringIO，
不过这取决你的Python安装版本，你可以优先使用cStringIO然后是StringIO（如果cStringIO不能用的话)。
在Python3中，Unicode是默认的string类型，但是如果你做任何和网络相关的操作，
很有可能你不得不用ASCII/字节字符串来操作，所以代替StringIO，你要io.BytesIO，为了达到你想要的，
这个导入看起来有点丑：
from io import BytesIO as StringIO

try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
'''

def CheckCode(request):
    mstream = StringIO.StringIO()
    validate_code = Checkcode.create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
    
    #将验证码保存到session
    request.session["CheckCode"] = validate_code[1]
    
    return HttpResponse(mstream.getvalue()) 


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        check_code = request.POST.get('checkcode')
        #从session中获取验证码
        session_code = request.session["CheckCode"]
        if check_code.strip().lower() != session_code.lower():
            return HttpResponse('验证码不匹配')
        else:
            return HttpResponse('验证码正确')          
        
    return render_to_response('login.html',{'error':"",'username':'','pwd':'' })

