# HexOcean-recruitment-task
## Running project
To create users and tier membership levels i used a Django admin
 ```
 docker build . 
 docker-compose run --rm app sh -c "python manage.py createsuperuser"
 docker-compose run --rm app sh -c "python manage.py makemigrations"
 docker-compose run --rm app sh -c "python manage.py migrate"
 docker-compose up
 ```
 Open for an API overview
 ```
 http://localhost:8000/swagger/
 ```
## Requirements of task:
- [X] it should be possible to easily run the project. docker-compose is a plus
- [X] users should be able to upload images via HTTP request
- [X] users should be able to list their images
- [X] there are three bultin account tiers: Basic, Premium and Enterprise:
- [X] users that have "Basic" plan after uploading an image get: 
- [X] a link to a thumbnail that's 200px in height
- [X] users that have "Premium" plan get:
- [X] a link to a thumbnail that's 200px in height
- [X] a link to a thumbnail that's 400px in height
- [X] a link to the originally uploaded image
- [X] users that have "Enterprise" plan get
- [X] a link to a thumbnail that's 200px in height
- [X] a link to a thumbnail that's 400px in height
- [X] a link to the originally uploaded image
- [ ] ability to fetch an expiring link to the image 
- [X] admins should be able to create arbitrary tiers with the following things configurable:
- [X] arbitrary thumbnail sizes
- [X] presence of the link to the originally uploaded file
- [ ] ability to generate expiring links
- [X] admin UI should be done via django-admin
- [ ] tests - (Not done yet.)
- [X] validation
- [X] performance considerations (assume there can be a lot of images and the API is frequently accessed)

## I would like to mention:
I connected PGadmin with Postgres container (I had some issues of django migrations).
I did not configure CI to this project because i am a newbie to Continous Integration (there was a attempt but with failure).
I consider about perfomance of that API, and I would choose Amazon S3 for larger scale project.
