# -----Импорт пакетов-------------------------------------------------------------
import json
import pprint
from pymongo import MongoClient

# -----Подключение----------------------------------------------------------------

# установить соединение с MongoClient
client = MongoClient(host='localhost', port=27017)

# удалить БД (каждый раз начинаем "с чистого листа")
client.drop_database('habr_news')

# создать БД
db = client['habr_news']

# создать коллекцию
collection = db.habr_news_collection

# ------Добавление------------------------------------------------------------------------------------------------------

# загрузить json полученный в результате работы scrapy
with open('./habr_news/habr_news/spiders/news.json', encoding='utf-8') as news_json_file:
    habr_news = json.load(news_json_file)

# добавить все данные из json в mongodb
db.habr_news_collection.insert_many(habr_news)

# ------Запросы---------------------------------------------------------------------------------------------------------

# количество документов в коллекции
print(f"Количество документов в коллекции: {db.habr_news_collection.count_documents({})}")

# получить имена коллекций из БД
print(f"Имена коллекций в БД: {db.list_collection_names()}")

# получить один любой документ из коллекции
print(f"Один любой документ из коллекции: {pprint.pformat(db.habr_news_collection.find_one())}")

# получить один документ из коллекции удовлетворяющий условию {'news_id': 529690}
print(f"Один документ с 'news_id' = 529690: {pprint.pformat(db.habr_news_collection.find_one({'news_id': 529690}))}")

# получить все документы из коллекции удовлетворяющие условию {'comments_counter': 3} + сортировка по 'news_id'
print("Все документы с количеством комметариев равным 3, отсортированные по 'news_id': ")
for item in db.habr_news_collection.find({'comments_counter': 3}).sort('news_id'):
    print(f"{pprint.pformat(item)}")

# получить все документы из коллекции удовлетворяющие условию {'author': 'avouner'}
print("Все документы с автором avouner: ")
for item in db.habr_news_collection.find({'author': 'avouner'}):
    print(f"{pprint.pformat(item)}")

# получить количество документов из коллекции
# поле tags которых содержит `Научно-популярное` (другие теги тоже допустимы)
print(f"Количество документов с тэгом 'Научно-популярное': "
      f"{db.habr_news_collection.count_documents({'tags': {'$all': ['Научно-популярное']}})}")

# ------Обновление------------------------------------------------------------------------------------------------------

# установить в качестве `author` имя `MONGO`
# во всех документах удовлетворяющие условию {'hubs': {'$all': ['Астрономия']}}
# и получить количество обновленных
update_result = db.habr_news_collection.update_many({'hubs': {'$all': ['Астрономия']}}, {'$set': {'author': 'MONGO'}})
print(f"Количество обновленных документов: {update_result.modified_count}")
# получить количество документов из коллекции, в которых 'author' = 'MONGO'
print(f"Количество документов с 'author' = 'MONGO': {db.habr_news_collection.count_documents({'author': 'MONGO'})}")

# ------Удаление--------------------------------------------------------------------------------------------------------

# удалить все документы, у которых 'comments_counter' равен 0
# и получить количество удаленных
print(f"Количество документов без комментариев: {db.habr_news_collection.count_documents({'comments_counter': 0})}")
print(f"Количество удаленных документов: {db.habr_news_collection.delete_many({'comments_counter': 0}).deleted_count}")
