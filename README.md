# The Platform
This repository refers to a simple, white-label, easily customizable course website.

Small note: The code was originally written in Brazillian Portuguese (varible names, hmtls files, etc). I did use GPT-6 Astra to translate all instances and remove some of my old not necessary themes. The rest of the code was entirely manually written. 

## Technologies
- Python 3.12 + Django 6
- Django Allauth (for authentication)
- Tailwind CSS (via CDN)
- Docker / Docker Compose

## Installation
**1. Clone the repo**

```bash
git clone https://github.com/kaner727/whitelabel-course-platform.git
cd whitelabel-course-platform
```

**2. Create and activate the virtual environmnet (venv)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Install the dependencies**

```bash
pip install -r requirements.txt
```

**4. Install Docker and run compose**

For this step, you will need to have Docker installed on your computer.
- For Windows and Mac, install Docker Desktop.
- For Linux, you can install either the Docker Engine (lightweight, cli-only version) or download Docker Desktop (GUI version).

After having downloaded and  configured Docker in your machine, run the following command:  
```
docker compose up -d 
```
Where "-d" is optional, it detaches your terminal/cli interface for running the next few commands.

**5. Migrate**
After having that complete, run:
```bash
python manage.py migrate
```
That command applies the migrations to the Postgres database. 

**6. Create a superuser**
```bash
python manage.py createsuperuser
```
Enter your username and password. Those credentials are important as they function in the log-in screen and (of course) are used to access superadmin functionalities inside the app. 

**7. Run server**
Finally, run the command below to start your local server:
```bash
python manage.py runserver
```
If everything is done correctly, the website should be available at http://127.0.0.1:8000/.

**8. After closing the application**
It is recommended that you run:
```bash
docker compose down
``` 
After you stop using the application. That stops the image of the databse to run in the background (consuming processing power of your machine).

If you want to delete ALL of the database, run:
```bash
docker compose down -v
``` 
That deletes all of the information you created while using the app. It will be necessary to run `py manage.py migrate` after if you want to re-initialize the application. 

## Content structure
     Courses
        └── Trails
            └── Modules
                └── Classes (video, text, activity/test, pdfs)

- **Course**: Holds the available Trails that the User can see. This is where the visual identity of the website is defined. 
- **Trail**: Holds modules. 
- **Module**: Holds classes and can have a cover image.
- **Class**: Where the content itself of the course is located. Superadmins can create classes of videos, text, pdfs and even tests.

To create, modify or delete any of the above mentioned structures, got to: `/superadmin/`.

## Creating a new Theme

Themes define the visual identity of the website for each user. Users with the same course have the same visual identity. 
dev disclaimer: I've tried doing this as simple as possible. Please pay attention to the following steps. 

**1. Create a new folder inside templates/themes**

Inside `templates/themes/`, create a new folder with your own theme slug:
templates/themes/your_theme/

**2. Crie os templates**

The folder HAS to contain these 6 html files:
- base_module.html
- dashboard.html
- module_empty.html
- text_lesson.html
- video_lesson.html
- choices_lesson.html

Use the files from `templates/themes/default/` as a base to create your new and fresh theme. 

**3. Register the theme in models.py**

In`members/models.py`, add the newly created theme in the variable `THEME_CHOICES` inside the class `Course`:

```python
THEME_CHOICES = [
    ('default', 'Padrão'),
    ('notdefault', 'Not default theme for tests'),
    ('your_theme', 'Name of my theme'),  # adicione aqui
]
```

**4. Run the migration**

```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Assign it to a Course**

In `/superadmin/manage_courses/`, select the new theme when creating or editing a course.
