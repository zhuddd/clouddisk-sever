from datetime import datetime
from typing import Union

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


class MyResponse(JsonResponse):


    def __init__(self, data:  Union[dict,str,int], status: bool, code: int = 200, **kwargs):
        rt = {"status": status, "code": code, "data": data, "time": str(datetime.now())}
        super().__init__(rt, **kwargs)

    @staticmethod
    def ERROR(data: Union[dict,str,int,list], code: int = 400):
        rt = {"status": False, "code": code, "data": data, "time": str(datetime.now())}
        return JsonResponse(rt, status=code)

    @staticmethod
    def ERROR404(request,msg: str = None):
        r=render(request, "404.html", {"msg": msg})
        r.status_code=404
        return r

    @staticmethod
    def SUCCESS(data:  Union[dict,str,int,list], code: int = 200):
        rt = {"status": True, "code": code, "data": data, "time": str(datetime.now())}
        return JsonResponse(rt, status=code)
