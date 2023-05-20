from flask import Blueprint,render_template,request,redirect
from .langchain import lang_chain


views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
def index():
    # print(request.method)
    if request.method == "POST":
        company = request.form.get('company')
        country = request.form.get('country')
        link = request.form.get('link')
        print(company)
        result = lang_chain(company=company,country=country)
        print(result)
    return render_template('index.html')


@views.route('company/',methods=['GET','POST'])
def out():
    if request.method == "POST":
        company = request.form.get('company')
        country = request.form.get('country')
        link = request.form.get('link')
        print(company)
        result = lang_chain(company=company.replace(' ','-'),country=country)
        print(result)
    return render_template('output.html',result)
