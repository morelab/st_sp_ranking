FROM python:3.8

RUN git clone https://github.com/morelab/st_sp_ranking.git
RUN mv st_sp_ranking app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

VOLUME ./config

CMD ["./run.sh"]

# docker run --network=iotoad_network -v $(pwd)/config:/app/config st_sp_ranking