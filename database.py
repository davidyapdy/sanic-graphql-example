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
