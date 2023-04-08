FROM python:3.9 as base

RUN pip install pipenv

RUN pip install psycopg2-binary

RUN apt-get update

RUN apt-get install -y git

RUN apt-get install -y ca-certificates curl apt-transport-https lsb-release gnupg
RUN  apt-get -y install azure-cli


ENV PROJECT_DIR=/usr/src/app
ENV SRC_DIR ${PROJECT_DIR}/src

COPY Pipfile ${PROJECT_DIR}/Pipfile
COPY Pipfile.lock ${PROJECT_DIR}/Pipfile.lock

WORKDIR ${SRC_DIR}
RUN git clone --recurse-submodules -j8 https://github.com/Chokhonelidze/ALLINONE.git

WORKDIR ${PROJECT_DIR}
RUN pipenv install --system --deploy
COPY  .  ${PROJECT_DIR}



EXPOSE 5000

CMD ["flask","run","-h", "0.0.0.0"]
