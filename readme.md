## Установка
    
    pip install django_mptt
    pip install -e git+https://github.com/openprofession/plp-eduplanner.git@master#egg=plp_eduplanner
    
#### INSTALLED_APPS
    mptt,plp_eduplanner

#### База данных
    ./manage.py migrate

#### Urls
    url('', include('plp_eduplanner.urls', namespace='plp_eduplanner')) добавить в urls.py



