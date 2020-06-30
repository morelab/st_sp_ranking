FROM python:3.8

RUN git clone https://github.com/morelab/st_sp_ranking.git
RUN mv st_sp_ranking app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

VOLUME ./config

CMD ["./run.sh"]

# docker run -v $(pwd)/config:/app/config --network toad_main_default --name st_sp_ranking st_sp_ranking