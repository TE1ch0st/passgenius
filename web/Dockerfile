FROM python:3.10.10-alpine3.17
LABEL authors="Vital"

RUN mkdir PassGenius
COPY . /PassGenius
COPY .. /PassGenius
WORKDIR /PassGenius
RUN pip3 install Flask~=2.2.3
RUN pip3 install gunicorn
EXPOSE 80

CMD ["python3", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:80", "--preload", "web_gui:app"]
