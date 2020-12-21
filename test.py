from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float,\
    ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer,primary_key=True)
    Genre = Column(String)

    def __repr__(self):
        return "<User(Genre='%s'')>" %(self.Genre)

class Movie(Base):
    """ Basic model holding `Products`.
        Note the relationship to `Departments`
    """
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    Genre_id = Column(Integer, ForeignKey('tags.id'))
    Genre = relationship("Tag", backref="movies")
    name = Column(String)
    director = Column(String)
    second_Genre = Column(String)
    IMDb_score = Column(Float)
    MC_score = Column(Float)
    year = Column(Float)

    def __repr__(self):
        return "<Movie(name='{}', director='{}', IMDb_score='{}',MC_score='{}',year='{}')>"\
                .format(self.name, self.director, self.IMDb_score, self.MC_score, self.year)

def drop_tables():
    """ Delete all tables...careful!
    """
    Base.metadata.drop_all(engine)


def create_tables():
    """ Initialize all the models in the database.
    """
    Base.metadata.create_all(engine)