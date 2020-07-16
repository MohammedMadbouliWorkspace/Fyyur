from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import *

db = SQLAlchemy()
migrate = Migrate(db=db)


class DBActionsExceptionsHandler:

    def __init__(self, session):
        self.session = session

    def fetch(self, origin):

        def wrapper(cls, **kwargs):
            try:
                data = origin(cls, **kwargs)
                return data

            except BaseException:
                self.session.close()
                return False

        return wrapper

    def change(self, origin):

        def wrapper(cls, **kwargs):

            try:
                origin(cls, **kwargs)
                self.session.commit()
                return True

            except BaseException:
                self.session.rollback()
                self.session.close()
                return False

        return wrapper


class DBActions:
    exception_handler = DBActionsExceptionsHandler(db.session)

    session = exception_handler.session

    @classmethod
    @exception_handler.fetch
    def get_one(cls, id):
        return cls.session.query(cls).filter(cls.id == id).first()

    @classmethod
    @exception_handler.fetch
    def get_all(cls, loadonly=None):
        if loadonly:
            return cls.query.options(loadonly).all()

        return cls.session.query(cls).all()

    @classmethod
    @exception_handler.fetch
    def get_filtered(cls, loadonly=True, filter=True):
        return cls.query.options(loadonly).filter(filter).all()

    @classmethod
    @exception_handler.change
    def add(cls, object_model=None, **kwargs):

        for key, value in kwargs.items():
            setattr(object_model, key, value)

        cls.session.add(object_model)

    @classmethod
    @exception_handler.change
    def add_all(cls, object_models=None, identifiers=None, **kwargs):

        for om, om_id in zip(object_models, identifiers):

            for key, value in kwargs.get(om_id):
                if value:
                    setattr(om, key, value)

        cls.session.add_all(object_models)

    @classmethod
    @exception_handler.change
    def remove(cls, object_model=None):
        cls.session.delete(object_model)

    @staticmethod
    def group_by_common(ilist, common_fields, group_name):
        def comp_factor(d, t):
            return tuple(d.__dict__.get(f) for f in t)

        return [
            {
                **dict(zip(common_fields, d1)),
                **{
                    group_name: [
                        d2 for d2 in ilist if comp_factor(d2, common_fields) == d1
                    ]
                }
            }
            for d1
            in
            set(
                comp_factor(d, common_fields) for d in ilist
            )
        ]

    @classmethod
    def search(cls, keyword):
        results = cls.get_filtered(
            loadonly=
            db.load_only(
                cls.id,
                cls.name
            ),
            filter=
            cls.name.ilike(
                f"%{keyword}%"
            )
        )

        return {
            "search_term": keyword,
            "status": "found" if results else "not_found",
            "count": len(results) if results else 0,
            "results": [
                {
                    "id": result.id,
                    "name": result.name,
                    "upcoming_shows_count": result.upcoming_shows_count
                } for result in (results if results else [])]
        }

    @classmethod
    def delete_ajaxly(cls, object_model, redir1, redir2):
        cached = {
            'name': object_model.name
        }

        status = cls.remove(object_model=object_model)

        return {
            'status': 'succeeded' if status else 'failed',
            'type': 'venue',
            'name': cached.get('name'),
            'redirection': redir1 if status else redir2
        }


class Profile(DBActions):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        nullable=False
    )

    city = db.Column(
        db.String(120),
        nullable=False
    )

    state = db.Column(
        db.Enum(
            State,
            name="state",
            validate_strings=True
        ),
        nullable=False
    )

    phone = db.Column(
        db.String(120)
    )

    genres = db.Column(
        db.ARRAY(
            item_type=db.Enum(
                Genres,
                name="genres",
                validate_strings=True,
            )
        ),
        nullable=False
    )

    website = db.Column(
        db.String(500)
    )

    image_link = db.Column(
        db.String(500)
    )

    facebook_link = db.Column(
        db.String(120)
    )

    seeking_description = db.Column(
        db.String()
    )

    shows = None

    @property
    def past_shows(self):
        return self.shows.filter(Show.start_time < datetime.now()).all()

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows(self):
        return self.shows.filter(Show.start_time >= datetime.now()).all()

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)


class Venue(db.Model, Profile):
    __tablename__ = 'Venue'

    address = db.Column(
        db.String(120),
        nullable=False
    )

    seeking_talent = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    shows = db.relationship(
        "Show",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )


class Artist(db.Model, Profile):
    __tablename__ = 'Artist'

    seeking_venue = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    shows = db.relationship(
        "Show",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )


class Show(db.Model, DBActions):
    __tablename__ = 'Show'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    venue_id = db.Column(
        db.Integer,
        db.ForeignKey("Venue.id"),
        nullable=False
    )

    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("Artist.id"),
        nullable=False
    )

    start_time = db.Column(
        db.DateTime,
        nullable=False
    )

    venue = db.relationship(
        "Venue",
        backref=db.backref("artists")
    )

    artist = db.relationship(
        "Artist",
        backref=db.backref("venues")
    )
