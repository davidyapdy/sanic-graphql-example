from sanic_graphql import GraphQLView
from sanic import Sanic
from practice_files.graphane_practice.app.database import db_session, init_db
from practice_files.graphane_practice.app.schema import schema

app = Sanic(__name__)
app.debug = True

default_query = """
{
    allEmployee {
        edges {
            node {
                id,
                name,
                department {
                    id,
                    name
                },
                role {
                    id,
                    name
                }
            }
        }
    }
}
""".strip()

app.add_route(GraphQLView.as_view(schema=schema, graphql=True, graphiq=True), '/graphql')

if __name__ == '__main__':
    init_db()
    app.run()
