Example Sanic + SQLAlchemy + Graphene (Graphql) Project
================================

This example project demos integration between Graphene, Sanic and SQLAlchemy.
The project contains two models, one named `Department`, `Role` and another
named `Employee`.

# sanic-graphql-example
Sanic example using Graphsql + SQLAlchemy

Run app.py and access via localhost:5000/graphql

## Required files
1. Graphene
2. Sanic
3. Graphene-Sqlalchemy
4. Sqlalchemy


#Tutzz
1. Build your model first
```python
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationships

from database import Base


# Basic SQLAlchemy
class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    department = relationships(
        Department,
        backref=backref('employee',
                        uselist=True,
                        cascade='delete,all'))
    role = relationships(
        Role,
        backref=backref('roles',
                        uselist=True,
                        cascade='delete,all'))

```
2. Initiate database + seed data + Commit
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Create database
engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


async def init_db():
    from models import Department, Employee, Role
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create Fixture for department
    engineering = Department(name='Engineering')
    db_session.add(engineering)
    hr = Department(name='Human Resource')
    db_session.add(hr)

    # Create Fixture for Role
    manager = Role(name='manager')
    db_session.add(manager)
    engineer = Role(name='Engineer')
    db_session.add(engineer)

    # Create
    peter = Employee(name='Peter', department=engineering, role=manager)
    db_session.add(peter)
    roy = Employee(name='Roy', department=engineering, role=engineer)
    db_session.add(roy)
    tracy = Employee(name='Tracy', department=hr, role=manager)
    db_session.add(tracy)

    # Insert seed data into database
    db_session.commit()
```
3. Define your scheme for graphql 
It is important to know some important terms here like *SQLAlchemyConnectionField* and *relay.Node*. Check out graphene official documentation for more info
```python
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_employee = SQLAlchemyConnectionField(Employee)
    all_roles = SQLAlchemyConnectionField(Role)
    role = graphene.Field(Role)


schema = graphene.Schema(query=Query, types=[Department, Employee, Role])
```
4. Let's run our Sanic App
```python
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

```
