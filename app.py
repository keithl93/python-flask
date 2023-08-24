from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('people', user='keith',
                        password='12345', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db

# Manga schema


class Manga(BaseModel):
    title = CharField()
    publication_year = IntegerField()

# Characters schema


class Characters(BaseModel):
    name = CharField()
    manga = CharField()
    age = IntegerField()


# Connection
db.connect()
db.drop_tables([Manga, Characters])
db.create_tables([Manga, Characters])

# create
Manga.create(title='One Piece', publication_year=1997)
Manga.create(title='Demon Slayer', publication_year=2016)

Characters(name='Roronoa Zoro', manga='One Piece', age='28').save()
Characters(name='Kamado Tanjiro', manga='Demon Slayer', age='16').save()
Characters(name='Monkey D. Luffy', manga='One Piece', age='24').save()
Characters(name='Kamado Nezuko', manga='Demon Slayer', age='14').save()

app = Flask(__name__)

# Manga endpoint


@app.route('/manga', methods=['GET', 'POST'])
@app.route('/manga/<id>', methods=['GET', 'PUT', 'DELETE'])
def manga_endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Manga.get(Manga.id == id)))
        else:
            manga_list = []
            for manga in Manga.select():
                manga_list.append(model_to_dict(manga))
            return jsonify(manga_list)

    if request.method == 'PUT':
        body = request.get_json()
        Manga.update(body).where(Manga.id == id).execute()
        return "Person" + str(id) + " has been updated."

    if request.method == 'POST':
        dict_to_model(Manga, request.get_json()).save()
        # new_manga.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Manga.delete().where(Manga.id == id).execute()
        return "Manga " + str(id) + " deleted."

# Characters endpoint


@app.route('/characters', methods=['GET', 'POST'])
@app.route('/characters/<id>', methods=['GET', 'PUT', 'DELETE'])
def characters_endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Characters.get(Characters.id == id)))
        else:
            character_list = []
            for character in Characters.select():
                character_list.append(model_to_dict(character))
            return jsonify(character_list)

    if request.method == 'PUT':
        body = request.get_json()
        Characters.update(body).where(Characters.id == id).execute()
        return "Person" + str(id) + " has been updated."

    if request.method == 'POST':
        dict_to_model(Characters, request.get_json()).save()
        # new_manga.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Characters.delete().where(Characters.id == id).execute()
        return "Characters " + str(id) + " deleted."


@app.route('/')
def index():
    return 'Welcome!'


app.run(port=2023, debug=True)
