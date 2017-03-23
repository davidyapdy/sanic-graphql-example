from sanic_graphql import GraphQLView
from sanic import Sanic
from database import db_session, init_db
from schema import schema

app = Sanic(__name__)
app.debug = True

# This will be the query
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

# It's like HTTP routes but instead, it directs you to /graphql (Schema).
# graphiq = True will initiate the GUI
app.add_route(GraphQLView.as_view(schema=schema, graphiql=True), '/graphql')

# runs the app and database. init_db contains seed data.
if __name__ == '__main__':
    init_db()
    app.run()
