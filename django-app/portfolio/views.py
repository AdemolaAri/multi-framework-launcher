from django.shortcuts import render
import json, pathlib
def index(request):
    cur = pathlib.Path(__file__).resolve().parent.parent
    content = json.load(open(cur/'shared'/'content.json'))
    return render(request,'portfolio/index.html',{'content':content})
