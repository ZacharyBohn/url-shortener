## Example Curl commands

First ensure that the application is running and connected to a database [see here for instructions on how to do that](README.md).

### Test communication to the server:

`curl localhost:8000/ping`

### Test creating a short url

`curl localhost:8000/shorten_url?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ`

### Test getting the original url

`curl -X GET "http://localhost:8000/redirect?short_url=[given short url here]`

### Test listing all urls in the database

`curl localhost:8000/list_urls`

### Test creating a short url with specified ID

`curl localhost:8000/shorten_url?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&short_url_id=136479`