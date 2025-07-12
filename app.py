from sanic_ext import Extend
from sanic import Sanic
from database import db_session, init_db
from schema import schema

app = Sanic(__name__)
Extend(app)
app.config.DEBUG = True

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

# Modern Sanic GraphQL integration using sanic-ext

@app.post("/graphql")
async def graphql_handler(request):
    from graphql import graphql
    query = request.json.get("query")
    variables = request.json.get("variables", {})
    result = await graphql(schema, query, variable_values=variables)
    return {"data": result.data, "errors": [str(e) for e in result.errors] if result.errors else None}

@app.get("/graphql")
async def graphql_playground(request):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GraphQL Playground</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            textarea { width: 100%; height: 300px; margin: 10px 0; }
            button { padding: 10px 20px; font-size: 16px; }
            .result { background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>GraphQL Playground</h1>
            <p>Try this query:</p>
            <textarea id="query">{ allEmployee { edges { node { id name department { name } role { name } } } } }</textarea>
            <br>
            <button onclick="runQuery()">Run Query</button>
            <div class="result" id="result">Results will appear here...</div>
        </div>
        <script>
            async function runQuery() {
                const query = document.getElementById('query').value;
                try {
                    const response = await fetch('/graphql', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query })
                    });
                    const result = await response.json();
                    document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """

# runs the app and database. init_db contains seed data.
if __name__ == '__main__':
    import asyncio
    asyncio.run(init_db())
    app.run(host="0.0.0.0", port=8000, debug=True)
