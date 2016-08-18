## Setting up a development environment

To setup a dev environment, first fork the cravattlab/cravattdb repository, then download [vagrant](https://www.vagrantup.com/downloads). You must also generate a SSH key and link it to your account. Github provides some [instructions](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) on doing this. To generate the key:

```bash
# we are providing an empty passphrase so that the VM can set itself up without requiring interaction
# for your personal key you may prefer to have a passphrase
ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -P ""
```

Then, change directories to your freshly cloned fork, and set a temporary environment variable called `private_key_file` pointing to your new private key. 

On Linux and OSX:
```bash
export private_key_file=/path/to/.ssh/id_rsa
```

On Windows, first make sure that you're in an administrative prompt (otherwise syncing will be problematic), and then:
```batch
set private_key_file=C:\Users\blergh\.ssh\id_rsa
```

Vagrant will pick the key up and make a copy inside the VM. Finally, run `vagrant up` and once the machine is done being setup, `vagrant ssh` to get access to the VM. If this fails, you can just use any ssh program and `ssh vagrant@127.0.0.1 -p 2222` with the default password `vagrant`.

Note that there will be two repositories shared into a folder called vagrant-sync. These are synced to the VM! Once the application has finished setting up, it will be accessible at (http://localhost:8080)[http://localhost:8080].

## Application Setup

Since we're now using LDAP for authentication some config is required. On development instances you must create a file `config/secrets.override.yml`. This will by default not be entered into version control. It must contain credentials for accessing Scripps Active Directory, example:

```yaml
flask-security:
  environment:
    SECURITY_LDAP_BIND_DN: 'radus@scripps.edu'
    SECURITY_LDAP_BIND_PASSWORD: 'MY_SCRIPPS_PASSWORD'
    SECURITY_PASSWORD_SALT: '8CjvYzVZgV8q:ZL#,7R8'
```
