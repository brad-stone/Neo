'''
Create virtualenv
    cd virtualenvs
    virtualenv neo
Activate virtualenv
    source neo/bin/activate
Install...
    pip install Flask
    pip install neo4j-driver
Start up Neo4j
    sudo service neo4j start
    test at http://localhost:7474
To run ...
    python neo.py
'''

from flask import Flask, g, Response, request
from neo4j.v1 import GraphDatabase, basic_auth
from json import dumps

app = Flask(__name__)
app.debug = True

password = "L0wt3ch!"

driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("neo4j", password))


def get_db ():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session ()
    return g.neo4j_db



@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()

@app.route("/")
def get_graph():
    db = get_db()
    testmovie = '"The Matrix"'
    results = db.run("MATCH (m:Movie) "
        "WHERE m.title =~ " + testmovie+ " "
        "RETURN m")
    return Response(results, mimetype="application/json")

'''

    results = '{"title": "The Matrix", "cast": [{"job": "acted", "role": ["Emil"], "name": "Emil Eifrem"}, {"job": "acted", "role": ["Agent Smith"], "name": "Hugo Weaving"}, {"job": "directed", "role": null, "name": "Andy Wachowski"}, {"job": "produced", "role": null, "name": "Joel Silver"}]}'
'''



'''
@app.route("/")
def get_graph():
    db = get_db()
    results = db.run("MATCH (m:Movie)<-[:ACTED_IN]-(a:Person) "
             "RETURN m.title as movie, collect(a.name) as cast "
             "LIMIT {limit}", {"limit": request.args.get("limit", 100)})
    nodes = []
    rels = []
    i = 0
    for record in results:
        nodes.append({"title": record["movie"], "label": "movie"})
        target = i
        i += 1
        for name in record['cast']:
            actor = {"title": name, "label": "actor"}
            try:
                source = nodes.index(actor)
            except ValueError:
                nodes.append(actor)
                source = i
                i += 1
            rels.append({"source": source, "target": target})
    return Response(dumps({"nodes": nodes, "links": rels}), mimetype="application/json")
'''


'''def hello():
    return "Hello World!"
'''

if (__name__ == "__main__"):
    app.run(port = 5000)
