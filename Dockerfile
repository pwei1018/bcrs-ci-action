FROM python:3.8.4-slim

RUN pip3 install pygithub

COPY pr_approval.py /pr_approval.py

ENTRYPOINT ["/pr_approval.py"]
