To setup from scratch, first we clone repos, and install docker:

```bash
sudo apt-get install -y git
mkdir ~/github && cd ~/github
git clone git@github.com:/cravattlab/cimage-minimal.git
git clone git@github.com:/cravattlab/cravatt-ip2.git

curl -sSL https://get.docker.com/ | sh
```

Before we build the docker images and run the containers, we must create a config file for cravattdb.

```bash
cd ~/github/cravatt-ip2/config
cp config.sample.py config.py
vi config.py
```

Then:

```bash
cd ~/github/cravatt-ip2
sudo docker build -t cravattdb_image .
sudo docker run -itd -p 5000:5000 -v $PWD/cravatt-ip2:/home/cravattdb/cravatt-ip2 -v $PWD/cimage-minimal:/home/cravattdb/cimage-minimal --name cravattdb cravattdb_image
```

Now we can run the necessary services:
```bash
sudo docker exec -d -u root cravattdb rabbitmq-server -detached
sudo docker exec -d cravattdb celery -A models.tasks worker --loglevel=info --detach
sudo docker exec -d cravattdb python index.py
```