# ----------------------------------------------------------------------------#
# Imports.
# ----------------------------------------------------------------------------#


import logging
from logging import Formatter, FileHandler
import babel
import dateutil.parser
from flask import Flask, render_template, request, flash, redirect, url_for, Markup, jsonify, json
from flask_moment import Moment
from models import *


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate.init_app(app)


# ----------------------------------------------------------------------------#
# Flash Messages Templates.
# ----------------------------------------------------------------------------#


def ACTION_SUCCEEDED(model_name, action, url=None, name=None):
    return Markup(
        f"""{model_name.capitalize()} {f'<a href="{url}">{name}</a>' if url else (name if name else '')} 
        was successfully {action}!"""
    )


def ACTION_FAILED(model_name, action, name=None):
    return Markup(
        f"An error occurred. {model_name.capitalize()} {name if name else ''} could not be {action}."
    )


def SHOW_CONFLICT_ERROR(artist, venue, show):
    return Markup(
        f"""There is already a show by
        <a href="{url_for("show_artist", artist_id=artist.id)}">{artist.name}</a>
        in <a href="{url_for("show_venue", venue_id=venue.id)}">{venue.name}</a>
        at {show.start_time}. You have to wait
        for it to end to post a new show."""
    )


FORM_VALIDATION_FAILED = "You have a problem with some of these fields."


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.after_request
def close_sqlalchemy_session(response):
    db.session.close()
    return response


#  Home Page.
#  ----------------------------------------------------------------
@app.route('/')
def index():
    """
    (1) Creates a route for Home page view
    :return: rendered HTML view for 'Home' page
    """
    return render_template('pages/home.html')


#  Indexes.
#  ----------------------------------------------------------------

#  # Venues Index.
#    --------------------------------------------------------------
@app.route('/venues')
def venues():
    """
    (1) Creates a route for Venues index view grouped by common cities
    :return: rendered HTML view for 'Venues' page
    """

    # fetch all minimized venues data and grouping it
    data = Venue.group_by_common(
        Venue.get_all(
            loadonly=db.load_only(
                Venue.id,
                Venue.name,
                Venue.city,
                Venue.state
            )
        ),
        ('city', 'state'),
        'venues'
    )

    # check if data is valid or exist
    if data:  # this returns True or False depending on query status
        return render_template('pages/venues.html', areas=data)

    else:
        return render_template("errors/500.html"), 500


#  # Artists index.
#    --------------------------------------------------------------
@app.route('/artists')
def artists():
    """
    (1) Creates a route for Artists index view
    :return: rendered HTML view for 'Artists' page
    """

    # fetch all minimized artists data
    data = Artist.get_all(
        loadonly=db.load_only(
            Artist.id,
            Artist.name
        )
    )

    # check if data is valid or exist
    if data:
        return render_template('pages/artists.html', artists=data)

    else:
        return render_template("errors/500.html"), 500


#  # Shows index.
#    --------------------------------------------------------------
@app.route('/shows')
def shows():
    """
    (1) Creates a route for Shows index view
    :return: rendered HTML view for 'Shows' page
    """

    # fetch all shows data
    data = Show.get_all()

    # check if data is valid or exist
    if data:
        return render_template('pages/shows.html', shows=data)

    else:
        return render_template("errors/500.html"), 500


#  Profiles.
#  ----------------------------------------------------------------

#  # Venue Profile.
#    --------------------------------------------------------------
@app.route('/profile/venue/<int:venue_id>')
def show_venue(venue_id):
    """
    (1) Creates a route for Venue profile view wih whole information related
    :param venue_id: (int) for get_one function to fetch data
    :return: rendered HTML view for 'Venue' page
    """

    # fetch one venue data by its id
    venue = Venue.get_one(id=venue_id)

    # check if data is valid or exist
    if venue:
        return render_template('pages/show_venue.html', venue=venue)

    else:
        return render_template('errors/404.html'), 404


#  # Artist Profile.
#    --------------------------------------------------------------
@app.route('/profile/artist/<int:artist_id>')
def show_artist(artist_id):
    """
    (1) Creates a route for Artist profile view wih whole information related
    :param artist_id: (int) for get_one function to fetch data
    :return: rendered HTML view for 'Artist' page
    """

    # fetch one artist data by its id
    artist = Artist.get_one(id=artist_id)

    # check if data is valid or exist
    if artist:
        return render_template('pages/show_artist.html', artist=artist)

    else:
        return render_template('errors/404.html'), 404


#  Creation Endpoints
#  ----------------------------------------------------------------


#  # Create Venue.
#    --------------------------------------------------------------
@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue():
    """
    (1) Creates a route for Create-New-Venue form view
    :return(GET): rendered HTML view for 'Post a venue' page
    :return(POST): redirections depending on form submission status
    """

    # initialize a form for post-venue-submission
    form = VenueForm(request.form)

    if request.method == 'GET':
        return render_template('forms/new_venue.html', form=form)

    elif request.method == 'POST':

        # validate the form
        if form.validate():

            # create a new venue instance
            venue = Venue()

            # fill venue data and check for creation status
            if venue.add(
                    object_model=venue,
                    name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    address=form.address.data,
                    phone=form.phone.data,
                    genres=form.genres.data,
                    website=form.website.data,
                    image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data,
                    seeking_talent=form.seeking_talent.data,
                    seeking_description=form.seeking_description.data
            ):

                flash(
                    ACTION_SUCCEEDED(
                        'venue',
                        'listed',
                        url_for("show_venue", venue_id=venue.id),
                        form.name.data
                    ),
                    category="alert-success"
                )

            else:

                flash(
                    ACTION_FAILED(
                        'venue',
                        'listed',
                        form.name.data
                    ),
                    category="alert-danger"
                )

        else:

            flash(
                FORM_VALIDATION_FAILED,
                category="alert-danger"
            )

            return redirect(url_for("create_venue"))

        return render_template('pages/home.html')


#  # Create Artist.
#    --------------------------------------------------------------
@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist():
    """
    (1) Creates a route for Create-New-Artist form view
    :return(GET): rendered HTML view for 'Post an artist' page
    :return(POST): redirections depending on form submission status
    """

    # initialize a form for post-artist-submission
    form = ArtistForm(request.form)

    if request.method == 'GET':
        return render_template('forms/new_artist.html', form=form)

    elif request.method == 'POST':

        # validate the form
        if form.validate():

            # create a new artist instance
            artist = Artist()

            # fill artist data and check for creation status
            if artist.add(
                    object_model=artist,
                    name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    phone=form.phone.data,
                    genres=form.genres.data,
                    website=form.website.data,
                    image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data,
                    seeking_venue=form.seeking_venue.data,
                    seeking_description=form.seeking_description.data
            ):

                flash(
                    ACTION_SUCCEEDED(
                        'artist',
                        'listed',
                        url_for("show_artist", artist_id=artist.id),
                        form.name.data
                    ),
                    category="alert-success"
                )

            else:

                flash(
                    ACTION_FAILED(
                        'artist',
                        'listed',
                        form.name.data
                    ),
                    category="alert-danger"
                )

        else:

            flash(
                FORM_VALIDATION_FAILED,
                category="alert-danger"
            )

            return redirect(url_for("create_artist"))

        return render_template('pages/home.html')


#  # Create Show.
#    --------------------------------------------------------------
@app.route('/shows/create', methods=['GET', 'POST'])
def create_show():
    """
    (1) Creates a route for Create-New-Show form view
    :return(GET): rendered HTML view for 'Post a show' page
    :return(POST): redirections depending on form submission status
    """

    # initialize a form for post-show-submission
    form = ShowForm(request.form)

    if request.method == 'GET':
        return render_template('forms/new_show.html', form=form)

    elif request.method == 'POST':

        # validate the form
        if form.validate():

            # get the wanted venue instance to link the show with
            venue = Venue.get_one(id=form.venue_id.data)

            # get the wanted artist instance to link the show with
            artist = Artist.get_one(id=form.artist_id.data)

            # create a new show instance
            show = Show()

            # check if there is already a show at time before the submitted show
            if db.session.query(Show).filter(
                    Show.venue_id == venue.id,
                    Show.artist_id == artist.id,
                    Show.start_time >= datetime.now()
            ).scalar() is not None:

                flash(
                    SHOW_CONFLICT_ERROR(artist, venue, Show.query.filter(Show.start_time >= datetime.now()).first()),
                    category="alert-warning"
                )

            else:

                # fill show, artist, venue data and check for creation status
                if Show.add_all(
                        object_models=[show, artist, venue],
                        identifiers=['s', 'a', 'v'],
                        s=[
                            ('start_time', form.start_time.data),
                            ('artist', artist),
                            ('venue', venue)
                        ],
                        a=[
                            (artist.shows.append(show), None)
                        ],
                        v=[
                            (venue.shows.append(show), None)
                        ]
                ):

                    flash(
                        ACTION_SUCCEEDED('show', 'listed'),
                        category="alert-success"
                    )

                else:

                    flash(
                        ACTION_FAILED('show', 'failed'),
                        category="alert-danger"
                    )

        else:

            flash(
                FORM_VALIDATION_FAILED,
                category="alert-danger"
            )

            return redirect(url_for("create_show"))

        return render_template('pages/home.html')


#  Editing Endpoints
#  ----------------------------------------------------------------


#  # Edit Venue.
#    --------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    """
    (1) Creates a route for Edit-Venue form view
    :param venue_id: (int) for get_one function to fetch data
    :return(GET): rendered HTML view for 'Edit profile' page
    :return(POST): redirections depending on form submission status
    """

    # initialize a form for edit-venue-submission
    form = VenueForm(request.form)

    # fetch one venue data by its id
    venue = Venue.get_one(id=venue_id)

    # check if data is valid or exist
    if venue:

        if request.method == 'GET':

            # populate venue form data to edit on it
            form.name.data = venue.name
            form.city.data = venue.city
            form.state.data = venue.state.name
            form.address.data = venue.address
            form.phone.data = venue.phone
            form.image_link.data = venue.image_link
            form.facebook_link.data = venue.facebook_link
            form.website.data = venue.website
            form.genres.data = [g.name for g in venue.genres]
            form.seeking_talent.data = venue.seeking_talent
            form.seeking_description.data = venue.seeking_description

            return render_template('forms/edit_venue.html', form=form, venue=venue)

        elif request.method == 'POST':

            if form.validate():

                # fill venue new data and check for update status
                if venue.add(
                    object_model=venue,
                    name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    address=form.address.data,
                    phone=form.phone.data,
                    genres=form.genres.data,
                    website=form.website.data,
                    image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data,
                    seeking_talent=form.seeking_talent.data,
                    seeking_description=form.seeking_description.data
                ):

                    flash(
                        ACTION_SUCCEEDED(
                            'venue',
                            'edited',
                            url_for("show_venue", venue_id=venue.id),
                            form.name.data
                        ),
                        category="alert-success"
                    )

                else:

                    flash(
                        ACTION_FAILED(
                            'venue',
                            'edited',
                            form.name.data
                        ),
                        category="alert-danger"
                    )

            else:

                flash(
                    FORM_VALIDATION_FAILED,
                    category="alert-danger"
                )

                return redirect(url_for("edit_venue", venue_id=venue_id))

            return redirect(url_for('show_venue', venue_id=venue_id))

    else:

        return render_template("errors/404.html"), 404


#  # Edit Artist.
#    --------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    """
    (1) Creates a route for Edit-Artist form view
    :param artist_id: (int) for get_one function to fetch data
    :return(GET): rendered HTML view for 'Edit profile' page
    :return(POST): redirections depending on form submission status
    """

    # initialize a form for edit-artist-submission
    form = ArtistForm(request.form)

    # fetch one artist data by its id
    artist = Artist.get_one(id=artist_id)

    # check if data is valid or exist
    if artist:

        if request.method == 'GET':

            # populate artist form data to edit on it
            form.name.data = artist.name
            form.city.data = artist.city
            form.state.data = artist.state.name
            form.phone.data = artist.phone
            form.image_link.data = artist.image_link
            form.facebook_link.data = artist.facebook_link
            form.website.data = artist.website
            form.genres.data = [g.name for g in artist.genres]
            form.seeking_venue.data = artist.seeking_venue
            form.seeking_description.data = artist.seeking_description
            return render_template('forms/edit_artist.html', form=form, artist=artist)

        elif request.method == 'POST':

            # validate the form
            if form.validate():

                # fill artist new data and check for update status
                if artist.add(
                        object_model=artist,
                        name=form.name.data,
                        city=form.city.data,
                        state=form.state.data,
                        phone=form.phone.data,
                        genres=form.genres.data,
                        website=form.website.data,
                        image_link=form.image_link.data,
                        facebook_link=form.facebook_link.data,
                        seeking_venue=form.seeking_venue.data,
                        seeking_description=form.seeking_description.data
                ):

                    flash(
                        ACTION_SUCCEEDED(
                            'artist',
                            'edited',
                            url_for("show_artist", artist_id=artist.id),
                            form.name.data
                        ),
                        category="alert-success"
                    )

                else:

                    flash(
                        ACTION_FAILED(
                            'artist',
                            'edited',
                            form.name.data
                        ),
                        category="alert-danger"
                    )

            else:

                flash(
                    FORM_VALIDATION_FAILED,
                    category="alert-danger"
                )

                return redirect(url_for("edit_artist", artist_id=artist_id))

            return redirect(url_for('show_artist', artist_id=artist_id))

    else:

        return render_template("errors/404.html"), 404


#  Ajax Endpoints
#  ----------------------------------------------------------------


#  # Search Venues.
#    --------------------------------------------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    (1) Creates an Endpoint for search implementation in ajax
    :return(POST): json response including
                   'search_term', 'status', 'count', 'results'
                   Go to `models.py` file to see details
                   about Model.search method.
    """

    # load data from request
    search_term = json.loads(request.data).get("search_term")

    # run search operation on Venue table and store results in response var,
    # see `models.py` for details.
    response = Venue.search(keyword=search_term)

    # check if there are any results
    if response.get('results'):
        return jsonify(response)

    else:
        return jsonify(response), 404


#  # Search Artists.
#    --------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    (1) Creates an Endpoint for search implementation in ajax
    :return(POST): json response including
                   'search_term', 'status', 'count', 'results'
                   Go to `models.py` file to see details
                   about Model.search method.
    """

    # load data from request
    search_term = json.loads(request.data).get("search_term")

    # run search operation on Artist table and store results in response var,
    # see `models.py` for details.
    response = Artist.search(keyword=search_term)

    # check if there are any results
    if response.get('results'):
        return jsonify(response)

    else:
        return jsonify(response), 404


#  # Delete Venue.
#    --------------------------------------------------------------
@app.route('/venues/<venue_id>/delete', methods=['GET', 'DELETE'])
def delete_venue(venue_id):
    """
    (1) Creates an Endpoint for delete implementation in ajax
    :param venue_id: (int) for get_one function to fetch data
    :return(GET): rendered HTML view for 'confirm deleting' page
    :return(DELETE): json response including
                   'status', 'type', 'name', 'redirection'
                   Go to `models.py` file to see details
                   about Model.delete_ajaxly method.
    """

    # fetch one venue data by its id
    venue = Venue.get_one(id=venue_id)

    # check if data is valid or exist
    if venue:

        if request.method == 'GET':
            return render_template("forms/delete_venue.html", venue=venue)

        elif request.method == 'DELETE':

            # run delete operation on Venue table and store results in response var,
            # see `models.py` for details.
            response = Venue.delete_ajaxly(
                object_model=venue,
                redir1=url_for("venues"),  # redirection link on success
                redir2=url_for("show_venue", venue_id=venue_id)  # redirection link on failure
            )

            # by deleting the venue, any associated shows will also be deleted automatically

            # check for deletion status to flash the right message
            if response.get("status") == "succeeded":

                flash(
                    ACTION_SUCCEEDED('venue', 'deleted', name=response.get('name')),
                    category="alert-success"
                )

            elif response.get("status") == "failed":

                flash(
                    ACTION_FAILED('venue', 'deleted', name=response.get('name')),
                    category="alert-danger"
                )

            return jsonify(response)

    else:

        return render_template("errors/404.html"), 404


#  # Delete Artist.
#    --------------------------------------------------------------
@app.route('/artists/<artist_id>/delete', methods=['GET', 'DELETE'])
def delete_artist(artist_id):
    """
    (1) Creates an Endpoint for delete implementation in ajax
    :param artist_id: (int) for get_one function to fetch data
    :return(GET): rendered HTML view for 'confirm deleting' page
    :return(DELETE): json response including
                   'status', 'type', 'name', 'redirection'
                   Go to `models.py` file to see details
                   about Model.delete_ajaxly method.
    """

    # fetch one artist data by its id
    artist = Artist.get_one(id=artist_id)

    # check if data is valid or exist
    if artist:

        if request.method == 'GET':
            return render_template("forms/delete_artist.html", artist=artist)

        elif request.method == 'DELETE':

            # run delete operation on Venue table and store results in response var,
            # see `models.py` for details.
            response = Artist.delete_ajaxly(
                object_model=artist,
                redir1=url_for("artists"),
                redir2=url_for("show_artist", artist_id=artist_id)
            )

            # by deleting the artist, any associated shows will also be deleted automatically

            # check for deletion status to flash the right message
            if response.get("status") == "succeeded":

                flash(
                    ACTION_SUCCEEDED('artist', 'deleted', name=response.get('name')),
                    category="alert-success"
                )

            elif response.get("status") == "failed":

                flash(
                    ACTION_FAILED('artist', 'deleted', name=response.get('name')),
                    category="alert-danger"
                )

            return jsonify(response)

    else:

        return render_template("errors/404.html"), 404


# ----------------------------------------------------------------------------#
# Error Handlers.
# ----------------------------------------------------------------------------#


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#


# Default port:
if __name__ == '__main__':
    app.run()


# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
