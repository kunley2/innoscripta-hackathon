from flask import Blueprint,render_template,request,redirect
from .langchain import lang_chain
from .manel import lang_model
import os
from dotenv import load_dotenv

load_dotenv()

google_cse_id = os.getenv('GOOGLE_CSE_ID')
google_api_key = os.getenv('GOOGLE_API_KEY')
openai_api_key = os.getenv("OPENAI_API_KEY")

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
        result = lang_model(company=company.replace(' ','-'),country=country,
                            openai_key=openai_api_key,google_api_key=google_api_key,google_cse_id=google_cse_id)
        # result = {'overview':f'{company}','products':'brandteon'}
        # print(result)
    return render_template('output.html',result=result,company=company)
