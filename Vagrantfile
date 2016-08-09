# -*- mode: ruby -*-
# vi: set ft=ruby :

private_key_file = ENV['private_key_file']
private_key = ''

if (private_key_file)
  private_key = File.read(private_key_file.chomp)
end

# check to make sure that we have vbguest installed
# this just makes syncing of folders work more reliably
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
    pip install docker-compose
    npm install -g typescript typings concurrently gulp

    # add vagrant user to docker group so we don't have to prefix every docker
    # command with sudo
    adduser vagrant docker
  SHELL

  config.vm.provision "ssh-setup", type: "shell", privileged: false, args: [private_key], inline: <<-SHELL
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh

    # save private key
    echo "$1" > ~/.ssh/github_rsa
    chmod 400 ~/.ssh/github_rsa

    {
      echo 'Host github.com'
      echo '  User git'
      echo "  IdentityFile ${HOME}/.ssh/github_rsa"
    } >> ~/.ssh/config

    chmod 600 ~/.ssh/config

    ssh-keyscan -H github.com >> ~/.ssh/known_hosts
    eval "$(ssh-agent)"
    ssh-add ~/.ssh/github_rsa
  SHELL

  config.vm.provision "code", type: "shell", privileged: false, inline: <<-SHELL
    # clone from cravattlab org
    git clone git@github.com:cravattlab/cimage-minimal.git ~/github/cimage-minimal
    git clone git@github.com:cravattlab/cravattdb.git ~/github/cravattdb
    # grab config from local fork
    cp -f /vagrant/.git/config ~/github/cravattdb/.git/config
  SHELL

  config.vm.provision "goodies", type: "shell", privileged: false, inline: <<-SHELL
    {
      echo "alias dc='docker-compose'"
      echo "alias ac='docker attach cravattdb_cravattdb_1'"
      echo "alias exc='docker exec -it cravattdb_cravattdb_1 /bin/bash'"
    } >> ~/.bashrc
  SHELL

  config.vm.provision "app-startup", type: "shell", privileged: false, inline: <<-SHELL
    cd ~/github/cravattdb && docker-compose up -d
    echo "Server should be accessible on http://localhost:8080!"
  SHELL

end