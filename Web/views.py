from flask import Blueprint,render_template,request,redirect
from .langchain import lang_chain
from .manel import lang_model


views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
def index():
    # print(request.method)
    if request.method == "POST":
        company = request.form.get('company')
        country = request.form.get('country')
        link = request.form.get('link')
    return render_template('index.html')


@views.route('company/',methods=['GET','POST'])
def out():
    if request.method == "POST":
        company = request.form.get('company')
        country = request.form.get('country')
        link = request.form.get('link')
        result = lang_model(company=company.replace(' ','-'),country=country)
        # result = {'overview':f'{company}','products':'brandteon'}
        # print(result)
    return render_template('output.html',result=result,company=company)
