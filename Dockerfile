FROM python:3.8.0
ADD . /fgm/
RUN pip install -r /fgm/requirements.txt
WORKDIR /fgm/
CMD ["python", "-m", "FootGramBot"]
