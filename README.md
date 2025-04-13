# NotateQ-API
**NotateQ-API** is a simple REST API for uploading, storing and downloading files from a server.

## Project setup
The following commands should be executed in a Python virtual environment.
### Installing required Python Packages
```
pip install -r requirements.txt
```
### Creating `.env` file
Create `.env` file in the `NotesApplication` directory with following variables:\
`ALLOWED_HOSTS` - A list of host/domain names the site can serve\
`ALLOWED_ORIGINS` - A list of host/domain names allowed to connect with API
`SECRET_KEY` -Django secret key

**PostgreSQL database variables**\
`DB_NAME` - The name of the database\
`DB_USER` - The user for the database\
`DB_PASSWORD` - The user's password\
`DB_HOST` - The database domain or IP address\
`DB_PORT` - By default, 5432

### Database migration
```
python manage.py migrate
```
### Running Django app
```
python manage.py runserver
```
### Redis servers installation
See [Redis documentation](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) for instructions.

Start Redis with following command:
```
redis-server
```

### Celery and Celery Beat
Start the Celery application in another terminal:
```
python -m celery -A NotesApplication worker --loglevel=info
```
On Windows, use this command instead:
```
python -m celery -A NotesApplication worker --loglevel=info -P solo
```
Start periodic task handling with Celery Beat in another terminal:
```
python -m celery -A NotesApplication beat --loglevel=info
```

## Docker installation
Instead of setting project manually, you can use Docker. 
### Create a `.env` file
Before build the containers, create a `.env` file with environment variables listed above.
### Build the Django app image
```
docker build -t django-docker .
```

### Build and start the containers with Docker Compose
```
docker compose up --build
```

### Run initial database migrations
After first build you need to run database migrations. You can do this from another terminal (or use the `-d` flag to run Docker Compose in detached mode and use the same terminal):
```
docker exec -it <django-docker-container-id> python manage.py migrate
```
Replace `<django-docker-container-id>` with the actual container ID or name. To find container id use:
```
docker ps
```
### Restart Docker Compose setup
After running migrations, you need to restart the containers:
```
docker compose restart
```
## Endpoints
### Upload a file
**Endpoint:** `POST /api/files/`\
**Request:** Form-Data\
**Required data:**\
`title` - The title of the note\
`description` - A short description of added note\
`category` - Categories assigned to the note\
`author` - [WIP] Author of the note\
`file` - The file being uploaded (must be `.docx`, `.pdf` or `.txt`)

**Response:** 
```json
{
    "id": 4,
    "title": "Title",
    "description": "Some description",
    "category": null,
    "author": "JJaneq",
    "upload_date": "2025-04-01T16:06:23.509266Z",
    "file": "http://localhost:8080/media/store/files/some_note.docx",
    "downloads": 0,
    "delete_time": null,
}
```
***Response Explanation***\
`id` - Identifier of the uploaded file. \
`title` - The title of the note.\
`description` - Description of added note.\
`category` - ID of category assigned to the note.\
`author` - Author of the note.\
`upload_date` - Timestamp when the file was uploaded.\n
`file` - URL where the file can be accessed\
`downloads` - The number of times the file has been downloaded.\
`tag_names` - A list of tags.\
`delete_time` - Timestamp when file will be deleted from database (null by default).

### Retrieve information about all files
**Endpoint:** `GET /api/files`

### Retrieve information about single file
**Endpoint:** `GET /api/files/{id}`

### Retrive information about categories
**Endpoint:** `GET /api/categories`

### Create new category
**Endpoint:** `POST /api/categories`

**Required data:**
```json
{
    "name": "mathematics"
}
```

**Response**
```json
{
    "id": 3,
    "name": "mathematics"
}
```

### Deleting single file
**Endpoint:** `DELETE /api/files{id}`\
The file with specified ID will not be deleted right away. Instead `delete_time` will be set to be deleted in 14 days.

### Download incrementation
**Endpoint:** `POST /api/files/{id}/increment_downloads`\
Increments the `downloads` count of the specified file by 1.

### Searching book informations
**Endpoint:** `GET /api/books/search/{title}`\
Returns up to 10 results:
```json
{
    {
        "title": "Slow Horses",
        "subtitle": "",
        "authors": [
            "Mick Herron"
        ],
        "publishedDate": "2010-06-01"
    }
}
```