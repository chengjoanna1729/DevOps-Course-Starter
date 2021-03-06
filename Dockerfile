FROM python:3.8.5-buster as base
WORKDIR /src
COPY poetry.lock pyproject.toml /src/

FROM base as production
RUN pip install poetry \
    && poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev
COPY . /src/
ENTRYPOINT gunicorn --bind 0.0.0.0:${PORT:-8000} wsgi:app

FROM base as development
RUN pip install poetry
RUN poetry install
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

FROM base as test
RUN pip install poetry
RUN poetry install
COPY . /src/

# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    rm /var/lib/apt/lists/* -vf &&\
    apt-get clean &&\
    apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install ./chrome.deb -y &&\
    rm ./chrome.deb

# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    echo "Installing chromium webdriver version ${LATEST}" &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
    apt-get install unzip -y &&\
    unzip ./chromedriver_linux64.zip
    
ENTRYPOINT ["poetry", "run", "pytest"]