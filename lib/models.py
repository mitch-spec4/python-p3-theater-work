from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for our models
Base = declarative_base()

# Define the Role class which represents the 'roles' table in the database
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)  # Primary key column
    character_name = Column(String)  # Column for the character name
    auditions = relationship('Audition', backref='role')  # Relationship to the Audition class

    # Method to get all actors for this role
    def actors(self):
        return [audition.actor for audition in self.auditions]

    # Method to get all locations for this role
    def locations(self):
        return [audition.location for audition in self.auditions]

    # Method to get the lead actor for this role
    def lead(self):
        for audition in self.auditions:
            if audition.hired:
                return audition
        return 'no actor has been hired for this role'

    # Method to get the understudy for this role
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) >= 2:
            return hired_auditions[1]
        return 'no actor has been hired for understudy for this role'

# Define the Audition class which represents the 'auditions' table in the database
class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer, primary_key=True)  # Primary key column
    actor = Column(String)  # Column for the actor's name
    location = Column(String)  # Column for the audition location
    phone = Column(Integer)  # Column for the actor's phone number
    hired = Column(Boolean, default=False)  # Column to indicate if the actor is hired
    role_id = Column(Integer, ForeignKey('roles.id'))  # Foreign key to the roles table

    # Method to mark the actor as hired
    def call_back(self):
        self.hired = True

# Create an SQLite database and the tables
engine = create_engine('sqlite:///theater.db')
Base.metadata.create_all(engine)

# Create a new session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Example usage
if __name__ == "__main__":
    # Create a new role
    role = Role(character_name="Hamlet")
    session.add(role)
    session.commit()

    # Create new auditions for the role
    audition1 = Audition(actor="jason Kamau ", location="kakamega", phone=254738292456, role_id=role.id)
    audition2 = Audition(actor="jessica wairimu", location="Nairobi", phone=254744258485, role_id=role.id)
    session.add(audition1)
    session.add(audition2)
    session.commit()

    # Mark the first audition as hired
    audition1.call_back()
    session.commit()

    # Retrieve and print role details
    retrieved_role = session.query(Role).filter_by(character_name="Hamlet").first()
    print(f"Role: {retrieved_role.character_name}")
    print(f"Actors: {retrieved_role.actors()}")
    print(f"Locations: {retrieved_role.locations()}")
    print(f"Lead: {retrieved_role.lead().actor if isinstance(retrieved_role.lead(), Audition) else retrieved_role.lead()}")
    print(f"Understudy: {retrieved_role.understudy().actor if isinstance(retrieved_role.understudy(), Audition) else retrieved_role.understudy()}")

    # Print all roles and auditions in the database
    all_roles = session.query(Role).all()
    all_auditions = session.query(Audition).all()

