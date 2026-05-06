# image for authentication test
FROM python:3.11-slim

RUN pip install requests

COPY authentication_test.py /authentication_test/exam_docker.py

WORKDIR /authentication_test/

CMD ["python", "exam_docker.py"]

LABEL test_type="authentication"

# image for authorization test
FROM python:3.11-slim

RUN pip install requests

COPY authorization_test.py /authorization_test/authorization_test.py

WORKDIR /authorization_test/

CMD ["python", "authorization_test.py"]

LABEL test_type="authorization"

# image for Content
FROM python:3.11-slim

RUN pip install requests

COPY content_test.py /content_test/content_test.py

WORKDIR /content_test/

CMD ["python", "content_test.py"]

LABEL test_type="content_test"