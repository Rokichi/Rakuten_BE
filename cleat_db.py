#pip3 install SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
import pandas as pd
import os
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

  def __init__(self, item_name=None, shop_name=None, purchase_date=None, expected_purchase_date=None, purchase_flg=None, subscription_flg=None,):
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

Base.metadata.create_all(bind=engine)

#テンプレートの作成
item = Item(item_name="バナナ", shop_name="まいばすけっと 北品川駅東店", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)
item = Item(item_name="コーヒー豆", shop_name="ライフ 東五反田店", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)
item = Item(item_name="コーヒーシュガー", shop_name="ライフ 東五反田店", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)
item = Item(item_name="クッキー", shop_name="ライフ 東五反田店", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)

item = Item(item_name="合挽き肉", shop_name="スーパーマルセン", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)
item = Item(item_name="玉ねぎ", shop_name="スーパーマルセン", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)
item = Item(item_name="ナツメグ", shop_name="スーパーマルセン", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)
item = Item(item_name="パン粉", shop_name="スーパーマルセン", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)

item = Item(item_name="カップラーメン", shop_name="まいばすけっと 横浜駅東店", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)
item = Item(item_name="トイレットペーパー", shop_name="まいばすけっと 横浜駅東店", purchase_date=datetime.datetime(2022, 8, 23), expected_purchase_date=datetime.datetime(2022, 9, 22), purchase_flg=False, subscription_flg=True)
db_session.add(item)
item = Item(item_name="ヘッドフォン", shop_name="ビックカメラアウトレット×ソフマップ 横浜ビブレ店", purchase_date=None, expected_purchase_date=None, purchase_flg=True, subscription_flg=False)
db_session.add(item)
item = Item(item_name="プリンターのインク", shop_name="ビックカメラアウトレット×ソフマップ 横浜ビブレ店", purchase_date=datetime.datetime(2022, 7, 30), expected_purchase_date=datetime.datetime(2022, 8, 29), purchase_flg=False, subscription_flg=True)
db_session.add(item)

db_session.commit()

remind = Remind(remind_name="品川駅", remind_latitude=35.629112, remind_longitude=139.7389313)
#db_session.add(remind)
#remind = Remind(remind_name="横浜駅", remind_latitude=35.46619953518658, remind_longitude=139.6220834558722)
db_session.add(remind)
#remind = Remind(remind_name="横浜駅", remind_latitude=35.46619953518658, remind_longitude=139.6220834558722)
#db_session.add(remind)

db_session.commit()

shop = Shop(shop_name="まいばすけっと 北品川駅東店", shop_latitude=35.62236023579725, shop_longitude=139.73974297289365)
db_session.add(shop)
shop = Shop(shop_name="ライフ 東五反田店", shop_latitude=35.62508029340338, shop_longitude=139.729869261042)
db_session.add(shop)

shop = Shop(shop_name="スーパーマルセン", shop_latitude=35.457968930489685, shop_longitude=139.60473275678245)
db_session.add(shop)
#shop = Shop(shop_name="ビックカメラアウトレット×ソフマップ 横浜ビブレ店", shop_latitude=35.46488760413696, shop_longitude=139.618175840142)
#db_session.add(shop)
#shop = Shop(shop_name="まいばすけっと 横浜駅東店", shop_latitude=35.46153342979692, shop_longitude=139.62027542668977)
#db_session.add(shop)


db_session.commit()