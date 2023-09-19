# traefik-fastapi

inspired by:  
https://testdriven.io/blog/fastapi-docker-traefik/  
and then went on to infuse stuff from this series:  
https://www.digitalocean.com/community/tutorial-series/how-to-create-web-sites-with-flask

But first, there are a few things that need to be corrected from the first article.  
- `netcat` needs to be `netcat-traditional`
- module versions might create trouble.  I fixed that by just removing the module versions.
```
$ cat requirements.txt 
asyncpg
fastapi==0.89.1
ormar==0.12.1
psycopg2-binary
uvicorn==0.20.0

```
- tiangolo's gunicorn/iuvicorn image borks on a Mac M1.
   - I don't know enough to get the full picture, but using a different image fixed it for me.
   - This image: https://hub.docker.com/r/tedivm/uvicorn-gunicorn
   - so where you see:
   `# FROM tiangolo/uvicorn-gunicorn:python3.11-slim`
   replace with:
   `FROM tedivm/uvicorn-gunicorn`

   

