from datetime import datetime
from enum import Enum
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL, Optional


class State(Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'


class Genres(Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    Hip_Hop = 'Hip-Hop'
    Heavy_Metal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    Musical_Theatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    R_and_B = 'R&B'
    Reggae = 'Reggae'
    Rock_n_Roll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'


state_choices = [(c.name, c.value) for c in State]
genres_choices = [(c.name, c.value) for c in Genres]


class ShowForm(Form):
    artist_id = StringField(
        'artist_id',
        validators=[DataRequired()]
    )

    venue_id = StringField(
        'venue_id',
        validators=[DataRequired()]
    )

    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )

    city = StringField(
        'city',
        validators=[DataRequired()]
    )

    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=state_choices
    )

    address = StringField(
        'address',
        validators=[DataRequired()]
    )

    phone = StringField(
        'phone',
        validators=[Optional()]
    )

    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=genres_choices
    )

    website = StringField(
        'facebook_link',
        validators=[URL(), Optional()]
    )

    image_link = StringField(
        'image_link',
        validators=[URL(), Optional()]
    )

    facebook_link = StringField(
        'facebook_link',
        validators=[URL(), Optional()]
    )

    seeking_talent = BooleanField(
        'seeking_talent',
        validators=[Optional()]
    )

    seeking_description = TextAreaField(
        "seeking_description",
        validators=[Optional()]
    )


class ArtistForm(Form):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )

    city = StringField(
        'city',
        validators=[DataRequired()]
    )

    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=state_choices
    )

    phone = StringField(
        'phone',
        validators=[Optional()]
    )

    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=genres_choices
    )

    website = StringField(
        'facebook_link',
        validators=[URL(), Optional()]
    )

    image_link = StringField(
        'image_link',
        validators=[URL(), Optional()]
    )

    facebook_link = StringField(
        'facebook_link',
        validators=[URL(), Optional()]
    )

    seeking_venue = BooleanField(
        'seeking_venue',
        validators=[Optional()]
    )

    seeking_description = TextAreaField(
        "seeking_description",
        validators=[Optional()]
    )
