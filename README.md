To setup a dev environment, download [vagrant](https://www.vagrantup.com/downloads) and then `vagrant up`. Once the machine is done being setup, you may `vagrant ssh` and get to work! Fill in some values for config files:

```bash
cd ~/github/cravatt-ip2/config
cp config.sample.py config.py
vi config.py
vi ~/database.yml
```

Then just run [`docker-compose`](https://docs.docker.com/compose):

```bash
cd ~/github/cravatt-ip2
sudo docker-compose up -d
```

Note that there will be two repositories shared into a folder called vagrant-sync. These are synced to the VM!