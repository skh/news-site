# news-site
News Site project with postgresql and flask

## Optional preparation steps

* Use the `rdb-lab-newsdata` vagrant box that has been provided
* `sudo apt-get update; apt-get upgrade` (maybe unnecessary, but I list it here just in case it matters)
* `sudo apt-get install python-pip` installs the `pip` package manager for python, which is not present on the box
* make sure port 5000 on the box is forwarded to the host somehow

## How to run this project:

* Check out or unpack this code in the base directory of that vagrant box, i.e. next to the `Vagrantfile`.
* run `vagrant up` and `vagrant ssh`
* `cd /vagrant/news-site`
* make sure requirements from `requirements.txt` are installed. This project uses `python3`
* Make app executable with `chmod 755 news.py`
* Run app in development web server with `./news.py`

If you are not running this project in vagrant, change the IP addresses the app is listening on in line 101 of `news.py` to `127.0.0.1`.
