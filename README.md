
![logo](https://raw.githubusercontent.com/kstroobants/cohouse-django/main/.github/images/logo.PNG)

# Cohouse Web App with Django
I have developped this Django web application to gain insights into building applications and enhance my Django development skills. It helps in the process of finding and renting rooms in a shared living environment. Powered by Django, a robust and scalable web framework, the application offers a seamless experience for individuals seeking affordable accommodation and a sense of community.

Using Django technology enables my application to provide a user-friendly interface with advanced search and filtering capabilities. By leveraging Django's scalability, my application can accommodate a growing user base, ensuring a wide range of room options and potential matches. Whether it's students, young professionals, or newcomers to a city, my Django-powered web application provides an unparalleled platform for finding affordable rooms, fostering a sense of community, and simplifying the shared living experience.

The code I have developed can be used by a wide range of individuals and organizations who are interested in creating a similar platform for renting rooms and facilitating shared living arrangements. Here are some potential users
- Entrepreneurs and Startups
- Real Estate and Property Management Companies
- Educational Institutions
- Community Organizations
- Individuals and Developers


## Tech Stack
- Python3
  - geocoder and folium for address functionality
- Django4
  - crispy_forms: user friendly forms;
  - django_cleanup: automatically remove images when objects are deleted;
  - phonenumber_field: phone number parsing;
  - django_filters: part of the filters when searching a room;
  - django_countries: country input choices;
  - django.contrib.gis: filter on distance from a place
- JavaScript
  - Indicating the active navigation bar tab;
  - Interactive displaying and removing the uploaded images
- HTML
- CSS / Bootstrap

## Demo

- The project is hosted on
https://kstroobants.pythonanywhere.com/. Have fun playing around!

- The deployed project does not contain the functionality to search rooms lying in a radius around a point (=e.g. Paris). The feature was removed due to the lack of file storage space and sudo rights to install django gis dependent packages on pythonanywhere. Also, Postgres is not available in the free version. So, here you can see the demo of what is pushed to github.
![cohouse_demo_distance_search](https://github.com/kstroobants/cohouse-django/assets/130580298/c2916b78-a38b-4295-9af7-4e719c231357)



## Installation

Clone the repository and install the requirements:

```bash
  git clone https://github.com/kstroobants/cohouse-django.git

  pip install virtualenv
  virtualenv env
  env\scripts\activate

  pip install -r requirements.txt
```

To run the App, use:
```bash
  python manage.py runserver
```

## Roadmap

- Messaging app to connect tenants with room authors;
- REST API with Django REST framework

## License

[MIT](https://choosealicense.com/licenses/mit/)
