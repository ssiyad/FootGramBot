FROM python:3.8.0
ADD ./ /opt/
ENV PYTHONPATH="/opt/"
RUN pip install -r /opt/requirements.txt
CMD ["python", "/opt/FootGramBot/__main__.py"]
