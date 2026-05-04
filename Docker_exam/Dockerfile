FROM python:3.11-slim

RUN pip install requests

COPY authentication_test.py /authentication_test/exam_docker.py

WORKDIR /authentication_test/

CMD ["python", "exam_docker.py"]

LABEL test_type="authentication"
