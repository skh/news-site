# news-site
News Site project with postgresql and flask

## Optional preparation steps

* Use the `rdb-lab-newsdata` vagrant box that has been provided
* `sudo apt-get update; apt-get upgrade` (maybe unnecessary, but I list it here just in case it matters)
* `sudo apt-get install python-pip` installs the `pip` package manager for python, which is not present on the box
* optional: `sudo apt-get install virtualenv`
* make sure port 5000 on the box is forwarded to the host somehow

## How to run this project:

* Check out or unpack this code in the base directory of that vagrant box, i.e. next to the `Vagrantfile`.
* run `vagrant up` and `vagrant ssh`
* `cd /vagrant/news-site`
* make sure requirements from `requirements.txt` are installed (or `. venv/bin/activate`)
* `python news.py`
