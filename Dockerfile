FROM winamd64/python
RUN python -m venv .venv
RUN pip install beautifulsoup
RUN pip install matplotlib scipy numpy