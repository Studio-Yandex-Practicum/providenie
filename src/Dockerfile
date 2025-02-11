FROM python:3.11-slim-bookworm

ENV WORKDIR /app
ENV USER admin

WORKDIR $WORKDIR

RUN apt update && \
    apt install -y netcat-traditional curl && \
    apt clean autoclean && apt autoremove --yes

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache

COPY . .

RUN groupadd -r $USER && \
    useradd -d $WORKDIR -r -g $USER $USER && \
    chown $USER:$USER -R $WORKDIR && \
    chmod +x docker-entrypoint.bash

CMD ["./docker-entrypoint.bash"]
