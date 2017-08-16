Data Storage is a Django App consisting in a database with information about athletes and an API to search on this data.

It can be launched with Docker and these are the steps to get it up and running:
````
$ docker-compose build
$ docker-compose run ds ds-ctl migrate
$ docker-compose run ds ds-ctl createsuperuser
$ docker-compose run ds ds-ctl loaddata sample_data
$ docker-compose up
````

The application consists in two parts:
- <your_domain>/admin: standard django admin site.
- <your_domain>/api/athletes/search/: search API consisting in a single endpoint.

USAGE:
    method: POST
    body:
    {
       "name":  {"value":"Anna Gasser", "match":"exact"},
       "age": {"value": "18-21"},
       "skills": {"value":["winter sports","Cycling"]},
       "years_experience": {"value":10, "match":"exact"},
       "ids_only": false
    }

All the parameters are optional and can be combined. If none of them is provided all the athletes are returned.

- name:
    Returns all athletes that contain the searched "value" in their full name.
    The values of "match" choice can be exact/iexact/icontains.
- age:
    Returns all the athletes with age between or equals the range specified in "value".
    Where ranges can be: <18, 18-21, 22-25, 26-30, >30.
- skills:
    Returns all the athletes that contain at least one of the listed skills or any of their children.
- years_experience:
    Returns all athletes that have the years of experience specified in "value".
    The type of matches that can be performed are exact/lower/higher.
- ids_only:
    When ids_only is true only the ids of the athletes are returned, otherwise all the details are included.

Some improvements that could be done:
- Implement 'name' search using a trie.
- Authentication to prevent external people to access the data.
- More search criteria.
- Build a CSV uploader to add new data in bulk.
- Improve django admin to use widgets that perform better when there is a lot of data, like FilteredSelectMultiple
  or ManyToManyRawIdWidget for ManyToMany fields. Also the skills can be displayed in a tree using MPTTModelAdmin.

And some things more related to any Django app:
- Write unittests.
- Localise strings.
- Add proper code documentation not just inline comments.
- Add created_at and updated_at fields to all the models.

Some assumptions I made:
- Championships for current year don't count as experience. For example, being in 2017, an athlete whose first
  competition was in 2016 would have 1 year experience, but if the only competition is for 2017 that means 0 years.
- For simplicity I assumed that the max age of an athlete is 99 and the oldest championships are from 1900, but that can
  be easily changed.
- When returning the athletes data I return only the skills selected for the user even though we search on all of them.
  For example: if an athlete has only "skiing" skill I only return that in the dictionary but the athlete would be
  included in the search of athletes with "winter sport" skills.


Some decisions taken:
- About the tools and libraries:
    - I decided to use Django because it allows me to create a web app with an admin site just out of the box and it has
      some libraries I knew would be very useful in this case like the djangorestframework to build the API and
      django-mptt to create a tree for the skills.
    - I also used serializers because they make handling and validating API data very easy.
    - The decision about using Docker was simply because it was easy to set it up and I'm used to it.
    - I built an API because it's a very easy way to query data that can be used by external applications too but also
      because it's faster than building a graphical user interface :)
- About the queries:
    - I used the Django ORM because it makes querying very simple and it makes the code cleaner, easier to understand
      and a lot easier to refactor that using raw queries. But if the volume of data is very big maybe these queries
      should be analysed to see if the ORM is doing a good job or it's worth implementing the queries manually.
      When possible, I'm always in favour of the ORM.
    - Also in the search endpoint I tried to order the criteria so the ones that filter out more athletes are executed
      first to try to minimise the querying time, but I didn't make any analysis on the actual queries.
- About the models:
    - I tried to design them in a way that makes sense and also minimises queries. That is why I used a tree to optimise
      the skills search and I added indexes in all fields that could be searchable.
    - In Championships I decided to separate the year from the name to make the queries easier. I could have created one
      entry per Championship with a list of years (or ManyToMany relationship to the actual year of that championship)
      but I didn't consider it necessary as there is no other data related to Championships in this exercise, so having
      them as different entries made the search simpler.
- About the API:
    - My first idea was to implement the endpoint as a GET with the search criteria in the parameters, because GET is
      the usual method to just retrieve data while POST should be used for creation. But I changed my mind in the end
      and I decided that in this particular case is better to be able to post a dictionary so we can have more
      complicated criteria and a nicer way to make the search. So I look at it as an endpoint that "creates" a search
      (which is something that could be done in the future if the app is extended to log all the searches and results).
    - For skills search, I'd usually search by id, if the call is made from an app that already knows all the
      possibilities, as it's faster and you don't need to deal with capital letters or similar versions of a word, etc.
      But I decided to use skill names instead because it makes more sense from a user perspective if we consider the
      search API as a standalone.
