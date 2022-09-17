# -*- coding: utf-8 -*-
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum


recipes = {
    "recipe":[
    {
        "id": "1",
        "title": "チキンカレー",
        "making_time": "45分",
        "serves": "4人",
        "ingredients": "玉ねぎ,肉,スパイス",
        "cost": "1000"
    },
    {
        "id": "2",
        "title": "オムライス",
        "making_time": "30分",
        "serves": "2人",
        "ingredients": "玉ねぎ,卵,スパイス,醤油",
        "cost": "700"
    },
    ]
}

now_id = 2
app = FastAPI()


post_error_content = {
    "message": "Recipe creation failed!",
    "required": "title, making_time, serves, ingredients, cost"
}


def get_time_str():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def search_recipes(id:str):
    for i in range(len(recipes["recipe"])):
        if recipes["recipe"][i]['id'] == id:
            return i
    else:
        return 0


def check_recipes(id:str):
    for i in range(len(recipes["recipe"])):
        if recipes["recipe"][i]['id'] == id:
            return i
    else:
        return None


@app.get("/")
async def returnError():
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/recipes")
async def check_and_response(title:str=None, making_time:str=None, serves:str=None, ingredients:str=None, costs:str=None):
    global now_id, recipes
    if title is None or serves is None or serves is None:
            return JSONResponse(status_code=404, content=post_error_content)
    else:
        resp_to_post = {
            "id": 3,
            "title": None,
            "making_time": None,
            "serves": None,
            "created_at": "2016-01-12 14:10:12",
            "updated_at": "2016-01-12 14:10:12"
        }
        now_time = get_time_str()
        now_id += 1
        resp_to_post['id'] = str(now_id)
        resp_to_post['title'] = title
        resp_to_post['making_time'] = making_time
        resp_to_post['serves'] = serves
        resp_to_post['ingredients'] = ingredients
        resp_to_post['costs'] = costs
        resp_to_post['created_at'] = now_time
        resp_to_post['updated_at'] = now_time
        recipes['recipe'].append(resp_to_post)
        return {"message": "Recipe successfully created!", "recipe": [resp_to_post] }


@app.get("/recipes")
def read_recipes():
    return recipes

@app.get("/recipes/{id}")
def read_recipe_from_id(id:int=1):
    if id:
        return {"message": "Recipe details by id","recipe": [recipes['recipe'][search_recipes(str(id))]]}
    else:
        return {"message": "Recipe details by id","recipe": [recipes['recipe'][search_recipes('1')]]}


@app.patch("/recipes/{id}")
def change_recipes(id:int=1, title:str=None, making_time:str=None, serves:str=None, ingredients:str=None, cost:str=None):
    global recipes
    if id:
        id = search_recipes(str(id))
    else:
        id = 1
    if title is not None: recipes["recipe"][id]['title'] = title
    if making_time is not None: recipes["recipe"][id]['making_time'] = making_time
    if serves is not None: recipes["recipe"][id]['serves'] = serves
    if ingredients is not None: recipes["recipe"][id]['ingredients'] = ingredients
    if cost is not None: recipes["recipe"][id]['cost'] = cost
    return   { "message": "Recipe successfully updated!", "recipe": [recipes["recipe"][id]]}


@app.delete("/recipes/{id}")
def del_recipes(id:int=1):
    global recipes
    if id:
        id = check_recipes(str(id))
        if id is not None:
            recipes["recipe"].pop(id)
            return { "message": "Recipe successfully removed!" }
    return { "message":"No Recipe found" }


handler = Mangum(app)
