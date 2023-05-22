from Web import create_app
# from fastapi import FastAPI
# from fastapi.middleware.wsgi import WSGIMiddleware
# import uvicorn
from typing import Optional
from Web.langchain import lang_chain

# api = FastAPI()
flask_app = create_app()
# api.mount('/',WSGIMiddleware(flask_app))

if __name__ == '__main__':
    flask_app.run(debug=True)

# api_route = '/api/v1'

# @api.post(f'{api_route}/company')
# async def company(company:str,country:str,url:Optional[str]=None):
#     # print(url)
#     # result = lang_chain(company,country)
#     return {'result':'hello'}


# if __name__ == '__main__':
#     uvicorn.run(api)