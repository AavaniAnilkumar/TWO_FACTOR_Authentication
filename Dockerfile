FROM python:3.10
COPY . . 
EXPOSE 500
CMD ["flask","run","--host","0.0.0.0"]