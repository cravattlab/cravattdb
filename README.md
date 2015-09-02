To setup from scratch, first we clone repos, and install docker, and docker-compose

```bash
sudo apt-get install -y git, pip
mkdir ~/github && cd ~/github
git clone git@github.com:/cravattlab/cimage-minimal.git
git clone git@github.com:/cravattlab/cravatt-ip2.git

sudo pip install docker-compose
curl -sSL https://get.docker.com/ | sh
```

Before we build the docker images and run the containers, we must create a config file for cravattdb. Also, set a password for the postgres user in 
`docker-compose.yml`.

```bash
cd ~/github/cravatt-ip2/config
cp config.sample.py config.py
vi config.py
vi ~/github/cravatt-ip2/docker-compose.yml
```

Then just run [`docker-compose`](https://docs.docker.com/compose):

```bash
sudo docker-compose up -d
```