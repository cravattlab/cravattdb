To setup a dev environment, download [vagrant](https://www.vagrantup.com/downloads) and then `vagrant up`. Once the machine is done being setup, you may `vagrant ssh` and get to work by running [`docker-compose`](https://docs.docker.com/compose):

```bash
cd ~/github/cravattdb
sudo docker-compose up -d
```

Note that there will be two repositories shared into a folder called vagrant-sync. These are synced to the VM!