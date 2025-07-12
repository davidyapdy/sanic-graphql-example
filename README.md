# Sanic + SQLAlchemy + GraphQL Example

A modern, fully updated example project demonstrating integration between **Sanic**, **SQLAlchemy**, and **GraphQL** using Graphene.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![Sanic Version](https://img.shields.io/badge/sanic-23.12.1-green.svg)](https://sanic.dev)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit http://localhost:8000/graphql to access the GraphQL playground.

## 📋 Features

- **Modern Sanic 23.x** with sanic-ext integration
- **SQLAlchemy 1.4** with SQLite database
- **GraphQL API** with relay-style connections
- **Interactive GraphQL Playground** in browser
- **Sample data** with employees, departments, and roles
- **Fully updated dependencies** (2024-ready)

## 🏗️ Project Structure

```
├── app.py           # Main Sanic application
├── models.py        # SQLAlchemy database models
├── database.py      # Database configuration and initialization
├── schema.py        # GraphQL schema definitions
└── requirements.txt # Python dependencies
```

## 📊 Database Models

The project includes three interconnected models:

- **Department**: Company departments (Engineering, HR, etc.)
- **Role**: Job roles (Manager, Engineer, etc.)  
- **Employee**: Staff members with department and role relationships

## 🔍 GraphQL Queries

### Get All Employees
```graphql
{
  allEmployee {
    edges {
      node {
        id
        name
        hiredOn
        department {
          name
        }
        role {
          name
        }
      }
    }
  }
}
```

### Get All Departments
```graphql
{
  allDepartments {
    edges {
      node {
        id
        name
      }
    }
  }
}
```

### Get All Roles
```graphql
{
  allRoles {
    edges {
      node {
        id
        name
      }
    }
  }
}
```

## 🛠️ Dependencies

- **Sanic 23.12.1** - Modern Python web framework
- **SQLAlchemy 1.4.54** - Database ORM
- **Graphene 2.1.9** - GraphQL framework
- **graphene-sqlalchemy 2.3.0** - SQLAlchemy integration for Graphene
- **sanic-ext 23.12.0** - Sanic extensions

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/graphql` | GraphQL Playground (Interactive UI) |
| POST | `/graphql` | GraphQL API endpoint |

## 💡 Development Guide

### 1. Database Models (`models.py`)
Define your SQLAlchemy models with relationships:

```python
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship

class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    
    # Relationships
    department = relationship(Department, backref='employees')
    role = relationship(Role, backref='employees')
```

### 2. GraphQL Schema (`schema.py`)
Create GraphQL types from SQLAlchemy models:

```python
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    all_employee = SQLAlchemyConnectionField(Employee)
```

### 3. Sanic Application (`app.py`)
Modern Sanic setup with GraphQL endpoints:

```python
from sanic import Sanic
from sanic_ext import Extend

app = Sanic(__name__)
Extend(app)

@app.post("/graphql")
async def graphql_handler(request):
    query = request.json.get("query")
    result = await graphql(schema, query)
    return {"data": result.data}
```

## 🚦 Sample Data

The application automatically creates sample data:

**Departments:**
- Engineering
- Human Resources

**Roles:**
- Manager
- Engineer

**Employees:**
- Peter (Engineering Manager)
- Roy (Software Engineer)
- Tracy (HR Manager)

## 🔄 What's Updated

This project has been modernized from the original 2016 version:

- ✅ **Sanic 0.4 → 23.12.1** (Modern async web framework)
- ✅ **SQLAlchemy 1.0 → 1.4** (Latest compatible version)
- ✅ **Replaced deprecated sanic-graphql** with sanic-ext
- ✅ **Fixed async/await patterns**
- ✅ **Updated GraphQL playground**
- ✅ **Modern Python packaging**
- ✅ **Improved error handling**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
