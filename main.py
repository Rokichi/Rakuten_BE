from typing import Optional
from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
import pandas as pd
import os
import math

import datetime

database_file = os.path.join(os.path.abspath(os.getcwd()), 'data.bd')

engine = create_engine('sqlite:///' + database_file, convert_unicode=True, echo=True)

db_session = scoped_session(
    sessionmaker(
      autocommit = False,
      autoflush = False,
      bind = engine
    )
)

Base = declarative_base()
Base.query = db_session.query_property()

class Item(Base):
  #テーブルの名前
  __tablename__ = 'item_table'
  #columnの作成
  id = Column(Integer, primary_key=True)
  item_name = Column(String, unique = False)
  shop_name = Column(String, unique = False)
  purchase_date = Column(DateTime, unique = False)
  expected_purchase_date = Column(DateTime, unique = False)
  purchase_flg = Column(Boolean, unique = False)
  subscription_flg = Column(Boolean, unique = False)

  def __init__(self, item_name=None, shop_name=None, purchase_date=None, expected_purchase_date=None, purchase_flg=None, subscription_flg=None):
    self.item_name = item_name
    self.shop_name = shop_name
    self.purchase_date = purchase_date
    self.expected_purchase_date = expected_purchase_date
    self.purchase_flg = purchase_flg
    self.subscription_flg = subscription_flg

class Shop(Base):
  #テーブルの名前
  __tablename__ = 'shop_table'
  #columnの作成
  id = Column(Integer, primary_key=True)
  shop_name = Column(String, unique = False)
  shop_latitude = Column(Float, unique = False)
  shop_longitude = Column(Float, unique = False)
  

  def __init__(self, shop_name=None, shop_latitude=None, shop_longitude=None):
    self.shop_name = shop_name
    self.shop_latitude = shop_latitude
    self.shop_longitude = shop_longitude

class Remind(Base):
  #テーブルの名前
  __tablename__ = 'remind_table'
  #columnの作成
  id = Column(Integer, primary_key=True)
  remind_name = Column(String, unique = False)
  remind_latitude = Column(Float, unique = False)
  remind_longitude = Column(Float, unique = False)
  

  def __init__(self, remind_name=None, remind_latitude=None, remind_longitude=None):
    self.remind_name = remind_name
    self.remind_latitude = remind_latitude
    self.remind_longitude = remind_longitude

def make_docs(db):
    all_data = {"data":[]}

    for row in db:
        data = {
            "id": 0,
            "item_name": None,
            "shop_name": None,
            "purchase_date": None,
            "expected_purchase_date": None,
            "purchase_flg": None,
            "subscription_flg": None,
        }
        data['id'] = row.id
        data['item_name'] = row.item_name
        data['shop_name'] = row.shop_name
        data['purchase_date'] = row.purchase_date
        data['expected_purchase_date'] = row.expected_purchase_date
        data['purchase_flg'] = row.purchase_flg
        data['subscription_flg'] = row.subscription_flg

        all_data['data'].append(data)
    
    return all_data

def make_docs_shop(db):
    all_data = {"data":[]}

    for row in db:
        data = {
            "id": 0,
            "shop_name": None,
            "shop_latitude": None,
            "shop_longitude": None,
        }
        data['id'] = row.id
        data['shop_name'] = row.shop_name
        data['shop_latitude'] = row.shop_latitude
        data['shop_longitude'] = row.shop_longitude

        all_data['data'].append(data)
    
    return all_data

def make_docs_remind(db):
    all_data = {"data":[]}

    for row in db:
        data = {
            "id": 0,
            "remind_name": None,
            "remind_latitude": None,
            "remind_longitude": None,
        }
        data['id'] = row.id
        data['remind_name'] = row.remind_name
        data['remind_latitude'] = row.remind_latitude
        data['remind_longitude'] = row.remind_longitude

        all_data['data'].append(data)
    
    return all_data

app = FastAPI()

# データベースのテーブルアイテムの全てのデータを確認する
@app.get("/all")
async def Refister_item():

    db = db_session.query(Item).all()

    all_data = make_docs(db)
    
    return  all_data


# 買い物リストに追加
@app.post("/Register_item_list/{item_name}/{shop_name}")
async def Register_item(item_name: str, shop_name: str):
    db_check = db_session.query(Item).filter(Item.item_name == item_name).all()
    
    if (db_check == []):
        item = Item(item_name=item_name, shop_name=shop_name, purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
        db_session.add(item)
        db_session.commit()
    else:
        db = db_session.query(Item).filter(Item.item_name == item_name).first()
        db.shop_name = shop_name
        db.purchase_flg = True
        db.subscription_flg = False
        db_session.commit()

    db_check = db_session.query(Shop).filter(Shop.shop_name == shop_name).all()
    
    if (db_check == []):
        shop = Shop(shop_name=shop_name, shop_latitude=1000, shop_longitude=1000)
        db_session.add(shop)
        db_session.commit()
    
    db = db_session.query(Item).all()
    all_data = make_docs(db)
    
    return all_data

# サブスクリプションを変更する
@app.post("/Subscription_change/{item_name}")
async def Subscription_change(item_name: str):
    db = db_session.query(Item).filter(Item.item_name == item_name).first()
    if (db.subscription_flg == True):
        db.subscription_flg = False
    else:
        db.subscription_flg = True
    db_session.commit()
    
    db = db_session.query(Item).all()
    all_data = make_docs(db)
    
    return all_data

#　買い物リストから削除（データベースから削除)
@app.post("/Delete_item_list/{item_name}")
async def Refister_item(item_name: str):
    db_session.query(Item).filter(Item.item_name == item_name).delete()
    db_session.commit()

    db = db_session.query(Item).all()
    all_data = make_docs(db)
    
    return all_data


#購入処理
@app.post("/purchase_item/{item_name}/{purchase_date}")
async def Refister_item(item_name: str, purchase_date: str):
    purchase_date = datetime.datetime.strptime(purchase_date, '%Y-%m-%d')
    expected_purchase_date = purchase_date + datetime.timedelta(days=30)

    db = db_session.query(Item).filter(Item.item_name == item_name).first()
    db.purchase_flg = False
    db.purchase_date = purchase_date
    db.expected_purchase_date = expected_purchase_date
    db_session.commit()

    db = db_session.query(Item).all()
    all_data = make_docs(db)
    
    return all_data

# 店舗ごとの買い物リストの取得
@app.get("/item_by_store/{shop_name}")
async def item_by_store(shop_name:str):
    db = db_session.query(Item).filter(Item.shop_name == shop_name).filter(Item.purchase_flg == True).all()

    all_data = {"data":[]}

    for row in db:
        data = {
            "item_name": None,
        }
        data['item_name'] = row.item_name

        all_data['data'].append(data)

    return all_data

#リマインド位置の登録
@app.post("/Register_remind/{remind_name}/{latitude}/{longitude}/")
async def Register_remind(remind_name: str, latitude: float, longitude: float):
    db_check = db_session.query(Remind).filter(Remind.remind_name == remind_name).all()
    
    if (db_check == []):
        remind = Remind(remind_name=remind_name, remind_latitude=latitude, remind_longitude=longitude)
        db_session.add(remind)
        db_session.commit()
    else:
        db = db_session.query(Remind).filter(Remind.remind_name == remind_name).first()
        db.remind_name = remind_name
        db.remind_latitude = latitude
        db.remind_longitude = longitude

        db_session.commit()
    
    db = db_session.query(Remind).all()
    all_data = make_docs_remind(db)
    
    return all_data


#店舗位置の登録
@app.post("/Register_shop/{shop_name}/{latitude}/{longitude}")
async def Register_shop(shop_name: str, latitude: float, longitude: float):
    db_check = db_session.query(Shop).filter(Shop.shop_name == shop_name).all()
    
    if (db_check == []):
        shop = Shop(shop_name=shop_name, shop_latitude=latitude, shop_longitude=longitude)
        db_session.add(shop)
        db_session.commit()
    else:
        db = db_session.query(Shop).filter(Shop.shop_name == shop_name).first()
        db.shop_name = shop_name
        db.shop_latitude = latitude
        db.shop_longitude = longitude

        db_session.commit()
    
    db = db_session.query(Shop).all()
    all_data = make_docs_shop(db)
    
    return all_data

#商品一覧の取得
@app.get("/item_list")
async def item_by_store():
    db = db_session.query(Item).filter(Item.purchase_flg == True).all()
    data_by_store = make_docs(db)
    return data_by_store

from sqlalchemy import desc, asc

#　購入予定日が近い商品のリマインド
@app.get("/near_date/{date}")
async def item_by_store(date: str):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')

    db = db_session.query(Item).filter(Item.subscription_flg == True).filter(Item.purchase_flg == False).order_by(asc(Item.expected_purchase_date)).all()

    all_data = {"data":[]}
    
    for row in db:
        result = row.expected_purchase_date < date
        days_left = abs(row.expected_purchase_date - date)

        if (result == False):
            data = {
                "item_name": None,
                "days_left": None,
            }
            data['item_name'] = row.item_name
            data['days_left'] = days_left.days

            all_data['data'].append(data)

    return all_data

# リマインド場所での通知
@app.get("/remind_place/{latitude}/{longitude}")
async def remind_place(latitude:float,longitude:float):
    db = db_session.query(Remind).all()
    cnt=0
    all_data = {"data":[]}

    # 現在位置がリマインド位置に近いかを判定 (リマインド場所間は離れていることを想定)
    for row in db:
        remind_latitude=row.remind_latitude
        remind_longitude=row.remind_longitude
        distance=math.sqrt(((remind_latitude-latitude)**2)+((remind_longitude-longitude)**2))
        if(distance<0.010966):
            # リマインド場所と近い店舗を抽出
            db2 = db_session.query(Shop).all()
            for row2 in db2:
                shop_latitude=row2.shop_latitude
                shop_longitude=row2.shop_longitude
                dis2 = math.sqrt(((shop_latitude-remind_latitude)**2) + ((shop_longitude-remind_longitude)**2))
                if(dis2<0.10966):
                    # 店舗で買うべき商品があるかチェック
                    db3 = db_session.query(Item).all()
                    flg_store=0 # 店舗の重複を避ける
                    for row3 in db3:
                        # 店舗名が一致 かつ purchase_flg==true があれば、その店舗を通知
                        if((row2.shop_name==row3.shop_name)and(row3.purchase_flg == True)):
                            data = {
                                "shop_name": None,
                            }
                            data['shop_name'] = row3.shop_name
                            all_data['data'].append(data)
                            cnt+=1
                            flg_store=1
                            break        
    
    if(cnt==0):
        return None
        #return row2.shop_name
    else:
        return all_data

# 店舗にづいたら, 通知の機能
@app.get("/nearby_store/{latitude}/{longitude}")
async def nearby_store(latitude:float,longitude:float):
    db = db_session.query(Shop).all()
    cnt=0 # 現在地と近い店舗の数
    all_data = {"data":[]}

    for row in db:
        store_latitude=row.shop_latitude
        store_longitude=row.shop_longitude
        distance=math.sqrt(((store_latitude-latitude)**2)+((store_longitude-longitude)**2))
        #if(distance<0.005):
        if(distance<0.003):
            # 店舗で買うべき商品があるかチェック
            db3 = db_session.query(Item).all()
            flg_store=0 # 店舗の重複を避ける
            for row3 in db3:
                # 店舗名が一致 かつ purchase_flg==true があれば、その店舗を通知
                if((row.shop_name==row3.shop_name)and(row3.purchase_flg == True)):
                    data = {
                        "shop_name": None,
                    }
                    data['shop_name'] = row3.shop_name
                    all_data['data'].append(data)
                    cnt+=1
                    flg_store=1
                    break
    
    if(cnt==0):
        return None
    else:
        return all_data

# 買うべき商品のある店舗の一覧表示
@app.get("/shop_list")
async def shop_list():
    db = db_session.query(Shop).all()
    cnt=0 # 買うべき商品のある店舗の数
    all_data = {"data":[]}

    for row in db:
        # 店舗で買うべき商品があるかチェック
        db3 = db_session.query(Item).all()
        flg_store=0 # 店舗の重複を避ける
        for row3 in db3:
            # 店舗名が一致 かつ purchase_flg==true があれば、その店舗を通知
            if((row.shop_name==row3.shop_name)and(row3.purchase_flg == True)):
                data = {
                    "shop_name": None,
                }
                data['shop_name'] = row3.shop_name
                all_data['data'].append(data)
                cnt+=1
                flg_store=1
                break    
    if(cnt==0):
        return None
    else:
        return all_data

# 買うべき商品のない店舗の一覧表示
@app.get("/Done_shop_list")
async def Done_shop_list():
    db = db_session.query(Shop).all()
    cnt=0 # 買うべき商品のある店舗の数
    all_data = {"data":[]}

    for row in db:
        # 店舗で買うべき商品があるかチェック
        db3 = db_session.query(Item).all()
        flg_store=0 # 店舗の重複を避ける
        for row3 in db3:
            # 店舗名が一致 かつ purchase_flg==true があれば、その店舗を通知
            if((row.shop_name==row3.shop_name)and(row3.purchase_flg == True)):
                flg_store=1
                break
        
        if (flg_store == 0):
            data = {
                "shop_name": None,
            }
            data['shop_name'] = row.shop_name
            all_data['data'].append(data)
            cnt+=1
            flg_store=1
    
    if(cnt==0):
        return None
    else:
        return all_data

# 購入済みリストの取得
@app.get("/purchased")
async def purchased():
    db = db_session.query(Item).all()
    cnt=0 # 購入済みの商品の数
    all_data = {"data":[]}
    for row in db:
        if(row.purchase_flg==False):
            data = {
                    "item_name": None,
                    "shop_name": None,
                    "subscription_flg": None
                }
            data['item_name'] = row.item_name
            data['shop_name'] = row.shop_name
            data['subscription_flg'] = row.subscription_flg
            all_data['data'].append(data)
            cnt+=1
    if(cnt==0):
        return None
    else:
        return all_data

#　購入予定日が近くなった商品があることを通知
@app.get("/date_notification/{date}")
async def date_notification(date: str):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')

    db = db_session.query(Item).filter(Item.subscription_flg == True).filter(Item.purchase_flg == False).all()

    all_data = {"data":[]}
    cnt=0

    for row in db:
        days_left = abs(row.expected_purchase_date - date)
        result = row.expected_purchase_date < date

        if (days_left.days < 6 and result == False):
            data = {
                "item_name": None,
                "days_left": None,
            }
            data['item_name'] = row.item_name
            data['days_left'] = days_left.days

            all_data['data'].append(data)
            cnt+=1
    
    if(cnt==0):
        return None
    else:
        return all_data