from Web import create_app
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn
from Web.manel import lang_model,langchain_serp
from typing import Optional
import os

from dotenv import load_dotenv

load_dotenv()

google_cse_id = os.getenv('GOOGLE_CSE_ID')
google_api_key = os.getenv('GOOGLE_API_KEY')
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key_2 = os.getenv("OPENAI_API_KEY_2")
os.environ["SERPAPI_API_KEY"] = os.getenv('SERP_API_KEY')

api = FastAPI()
flask_app = create_app()


# if __name__ == '__main__':
#     flask_app.run(debug=True,host='0.0.0.0',port=5000)

api_route = '/api/v1'

@api.post(f'{api_route}/company')
async def company(company:str,country:str,url:Optional[str]=None):
    try:
        result = langchain_serp(company=company,country=country,
                            openai_key=openai_api_key)
    except:
        result = lang_model(company=company,country=country,
                            openai_key=openai_api_key_2,google_api_key=google_api_key,google_cse_id=google_cse_id)
    return {'result':result}

api.mount('/',WSGIMiddleware(flask_app))

if __name__ == '__main__':
    uvicorn.run(api,host='0.0.0.0',port=os.getenv("PORT"))