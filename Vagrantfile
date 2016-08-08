# -*- mode: ruby -*-
# vi: set ft=ruby :


required_plugins = %w(vagrant-vbguest)

plugins_to_install = required_plugins.select { |plugin| not Vagrant.has_plugin? plugin }
if not plugins_to_install.empty?
  puts "Installing plugins: #{plugins_to_install.join(' ')}"
  if system "vagrant plugin install #{plugins_to_install.join(' ')}"
    exec "vagrant #{ARGV.join(' ')}"
  else
    abort "Installation of one or more plugins has failed. Aborting."
  end
end

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"

  config.ssh.forward_agent = true
  config.vm.network "forwarded_port", guest:8080, host:8080

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end

  config.vm.synced_folder "vagrant-sync/cimage-minimal", "/home/vagrant/github/cimage-minimal", create: true
  config.vm.synced_folder "vagrant-sync/cravattdb", "/home/vagrant/github/cravattdb", create: true

  config.vm.provision "dependencies", type: "shell", inline: <<-SHELL
    # installing things
    add-apt-repository ppa:fkrull/deadsnakes
    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash

    apt-get update
    apt-get install -y git python-pip python3.5 cifs-utils nodejs

    curl -sSL https://get.docker.com/ | sh
    # add vagrant user to docker group so we don't have to prefix every docker
    # command with sudo
    adduser vagrant docker
    # update group for user so we don't have to log out before using docker commands
    # without sudo
    exec sudo su -l $USER
    pip install docker-compose
    npm install -g typescript typings concurrently gulp
  SHELL

  config.vm.provision "ssh-setup", type: "shell", privileged: false, inline: <<-SHELL
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    ssh-keyscan -H github.com >> ~/.ssh/known_hosts
    # suppress non-zero exit status so that vagrant continues to run other provisioners
    sh -c "ssh -T git@github.com; true"
  SHELL

  config.vm.provision "code", type: "shell", privileged: false, inline: <<-SHELL
    git clone git@github.com:cravattlab/cimage-minimal.git ~/github/cimage-minimal
    git clone git@github.com:cravattlab/cravattdb.git ~/github/cravattdb
    cp -f /vagrant/.git/config ~/github/cravattdb/.git/config
  SHELL

  config.vm.provision "goodies", type: "shell", privileged: false, inline: <<-SHELL
    echo "alias dc='docker-compose'" >> ~/.bashrc
    echo "alias ac='docker attach cravattdb_cravattdb_1'" >> ~/.bashrc
    echo "alias exc='docker exec -it cravattdb_cravattdb_1 /bin/bash'" >> ~/.bashrc
  SHELL

  config.vm.provision "app-startup", type: "shell", privileged: false, inline: <<-SHELL
    cd ~/github/cravattdb && docker-compose up -d
    echo "Server should be accessible on http://localhost:8080!"
  SHELL

end