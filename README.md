
Implementation of real-world application: https://github.com/gothinkster/realworld/ using Django and Unpoly.

An in-depth discussion of this implementation can be found [here](https://danjacob.net/posts/anatomyofdjangohtmxproject/).

Tech Stack:

* [Django](https://djangoproject.com)
* [Unpoly](https://unpoly.com)

To install and run locally:

```bash
git clone https://github.com/alnuaimi94/realworld/ && cd realworld

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

./manage.py migrate && ./manage.py runserver
```


**Note: this is just a reference implementation and is not intended for production use.**
