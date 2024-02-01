# jambopay-assessment
This is a Web App with Python and [Serverless Postgres](https://neon.tech/)

## Prerequisites
- Python experience i.e. [Django Framework](https://docs.djangoproject.com/en/4.2/)
- Basic understanding of HTML and CSS

## Getting Started
NOTE: Once you follow the below instructions, you should be able to run the application.

### Create dotenv file:
Run `echo "" > .env` to create the `.env` in the root of your project:

```bash
DATABASE_URL=""
DJANGO_SECRET_KEY=<some-secret>
DJANGO_DEBUG=1
ALLOWED_HOST="*"
```
Alternative to the above is having `.env-dev` or `.env-prod` with the above parameters set. Then `rav` command will handle the .env generation using `rav run server` command.

Replace `<some-secret>` by any of the following commands:

```bash
openssl rand -base64 32
```

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

```bash
python -c 'import secrets;print(secrets.token_urlsafe(32))'
```

=== Configure Environment

To install packages and run various command shortcuts, we use [rav](https://github.com/jmitchel3/rav). Open `rav.yaml` to see the various commands available if you prefer to not use `rav`.

_macOS/Linux Users_
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install pip pip-tools rav --upgrade
rav run installs
rav run freeze
```
In `rav.yaml`, you'll see that `rav run installs` maps to:

- `venv/bin/pip-compile src/requirements/requirements.in -o src/requirements.txt`
- `venv/bin/python -m pip install -r src/requirements.txt`
- `npm install`


_Windows Users_
```powershell
c:\Python310\python.exe -m venv venv
.\venv\Scripts\activate
python -m pip install pip pip-tools rav --upgrade
rav run win_installs
rav run win_freeze
```
In `rav.yaml`, you'll see that `rav run win_installs` maps to:

- `pip-compile src/requirements/requirements.in -o src/requirements.txt`
- `python -m pip install -r src/requirements.txt`
- `npm install`


=== Main Commands

With all the configuration done, here are the main commands you'll run:

```
rav run server
rav run watch
rav run vendor_pull
```

- `rav run server` maps to `python manage.py runserver` in the `src` folder
- `rav run watch` triggers tailwind to watch the tailwind input file to make the compiled tailwind output file via `npx tailwindcss -i <input-path> -o <output-path> --watch`
- `rav run vendor_pull` run this occasionally to pull the latest version of Flowbite, HTMX, and any other third party static vendor files you need.

## Application structure

The main source code sits in the `src` folder. The `src` folder contains the project directory `assignment` and a django app called `jambo`.
The folder `config` contains a script to be used when running Dockerfile. The `docs` folder contains the database design, the .dbml is generated from [dbdiagram.io](https://dbdiagram.io/) and the .sql is generated using the .dbml file as an input. The commands are in the `rav.yaml` file.
The `jambo` app contains custom user logic and custom user model with other models available to handle the data upload. It also contains a custom [materialised view](https://github.com/sreevardhanreddi/django-materialized-views) which i used to return data to the `user_business_list_view` in jambo app.

I managed to write minimal tests for the `views`` and `utils``, though i didn't want to take much time on that. However, it is necessary to write tests to cover all cases of whichever function was written. I also didn't manage to fix the UI much, i did the very basic setup to get the application working as expected. I'll revisit the UI at a later on.

I've uploaded images of how the application looks and functions once you've run the setup [above](#getting-started). Please consider the screenshots for your review as well as part of this submission.

NOTE:
I'll push .env-dev file for the assessment and there after i'll remove it after a period of 2 weeks.

## Incomplete
- User interface, managed to get the UI responsive but it took a while to correct issues experienced with tailwind. Hence the need to have commands setup using `rav`.
- I used built-in python library `csv` to handle csv. I would have traded it off with `pandas` to handle the uploads. The `CSVImportForm` validates the file extension, locked to `.csv` presently.