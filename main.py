from Web import create_app
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn
from Web.manel import lang_model
from typing import Optional
import os

api = FastAPI()
flask_app = create_app()


# if __name__ == '__main__':
#     flask_app.run(debug=True,host='0.0.0.0',port=5000)

api_route = '/api/v1'

@api.post(f'{api_route}/company')
async def company(company:str,country:str,url:Optional[str]=None):
    # print(url)
    result = lang_model(company=company.replace(' ','-'),country=country)
    return {'result':result}

api.mount('/',WSGIMiddleware(flask_app))

if __name__ == '__main__':
    uvicorn.run(api,host='0.0.0.0',port=os.getenv("PORT"))