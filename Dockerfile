FROM python:3.8.4-slim

RUN pip3 install pygithub==1.47

COPY compare_vaults.py /compare_vaults.py

ENTRYPOINT ["/compare_vaults.py"]
