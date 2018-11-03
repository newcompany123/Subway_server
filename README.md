# MySubway v1.0

MySubway is an app that you can keep your own recipe of Subway sandwich.\
You can also try a various type of sandwich recipes registered on the app.\
Even when you actually visit Subway, you can make good use of the app when ordering sandwich.\
Instead of being hesitating for yourself telling the clerk each ingredients of your sandwich, just read your saved recipe in MySubway.


<br>

## Used Skills

* Python 3.6.5
* Django 2.1.2
  - django-json-secrets 0.1.10
  - django-debug-toolbar 1.10.1
  - django-storages 1.6.6
* Django REST framework 3.8.2
  - django-filter 2.0.0
* AWS
  - Elastic Beanstalk
  - RDS(Relational Database Service)
  - S3
  - Route53
  - ACM (AWS Certificate Manager)
* Docker, Dockerhub
* OAuth (Web, iOS, Android)
  - Facebook Login
  - Kakao Login
* Database
  - Local(sqlite3)
  - Production & Dev(postgresql)
* Server
  - Nginx
* Git
  - Git Organization
  - Git Fork Repository
* etc
  - Sentry



<br>
<br>

---



# Code Review
* In this code review, the example codes have been simplified to make it easier to understand.

<br>

## 1. Facebook Login Test with access_token
This code doesn't follow common OAuth process of Facebook.\
It is because this test is implemented only in back-end area, not in front-end area.
Even if we make similar function with Django template, it doesn't guarantee the operation in front-end side.\
Instead, we use special test API from Facebook developer.

Shown below is a brief explanation of the review.

    1. First, get app_access_token from Facebook
    2. With the app_access_token, make a test-user
    3. When test user is made successfully, we can get general access-token from that test-user


In this code, we are going to use APITestCase from rest_framework.\
First, we need to set some necessary information.

```python
class FacebookLoginTest(APITestCase):

    # URL_HOST for local / staging test
    SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
    if SETTINGS_MODULE == 'config.settings.prod':
        from config.settings import prod
        URL_HOST = prod.URL_HOST
    else:
        from config.settings import local
        URL_HOST = local.URL_HOST

    URL_FACEBOOK_LOGIN = URL_HOST + reverse('user:facebook-login')
    URL_ACCESS_TOKEN = 'https://graph.facebook.com/v2.12/oauth/access_token'
```

Our Facebook Login API address is basic information.\
In this code, we assume that the user divided 'app.config.settings' into three parts: local, dev and prod(production).\
To make this test code available both in local and production environments, URL_HOST need to be set for each environment as the code above.


Now let's look at 'test_facebook_login' which is the main body of the test code.


```python
    def test_facebook_login(self):

        app_access_token = self.get_app_access_token_from_facebook()
        access_token = self.get_short_term_access_token_from_facebook(app_access_token)

        # Try Facebook Login API
        post_data = {
            'access_token': access_token
        }
        response = requests.post(self.URL_FACEBOOK_LOGIN, post_data)
```

It calls get_app_access_token_from_facebook.


```python
    def get_app_access_token_from_facebook(self):

        # Facebook client_credentials access
        params = {'client_id': settings.FACEBOOK_APP_ID,
                  'client_secret': settings.FACEBOOK_SECRET_CODE,
                  'grant_type': 'client_credentials'}
        response = requests.get(self.URL_ACCESS_TOKEN, params=params)
        response_dict = response.json()
        access_token = response_dict['access_token']
        return access_token
```

In the get_app_access_token_from_facebook method, it sends GET request with parameters including 'grant_type'.\
With the received response data, call _get_json.
_get_json method was made separately for json exception handling.

```python
    def _get_json(self, response):
        try:
            response_dict = response.json()
        except ValueError:
            raise CustomAPIException("Unexpected response. No JSON object could be decoded.")
        if 'error' in response_dict:
            raise CustomAPIException("Error in response: %r" % response_dict['error'])
        return response_dict
```

The response dict looks like this.

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

With this access_token, call get_short_term_access_token_from_facebook again in  test_facebook_login method.

```python
    def get_short_term_access_token_from_facebook(self, app_access_token):

        # Facebook app access token access
        url = f'https://graph.facebook.com/v2.12/{settings.FACEBOOK_APP_ID}/accounts/test-users'
        params = {'access_token': app_access_token}
        response = requests.get(url, params=params)

        response_dict = response.json()
        response_data = response_dict.get('data')[0]
        if response_data.get('id'):
            access_token = response_data.get('access_token')
            if not access_token:
                raise CustomAPIException("User %s located, but does not have access_token." % self.id)
            return access_token
        raise CustomAPIException("Unable to find user from response.")
```

In this code, it sends GET request with access_token parameters.\
Response data looks like this.

```json
{
    "data": [{
        "id": "...",
        "login_url": "https://developers.facebook.com/checkpoint/test-user-login/285792995586905/",
        "access_token": "EAATCQq7ICIsBALhe3sbP..."
        }],
    "paging": {
        "cursors": "..."
     }
}
```

Now we have normal access_token which we can test our own Facebook Login API.\
Test Facebook Login API request with access_token. And check the response data whether API works well.

```python
    def test_facebook_login(self):

        ...

        # Facebook Login API Test
        post_data = {
            'access_token': access_token
        }
        response = requests.post(self.URL_FACEBOOK_LOGIN, post_data)
        response_data = self._get_json(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['username'], 'Open')
        self.assertEqual(response_data['email'], '')

        # Delete User from the service
        headers = {
            'Authorization': 'Token ' + response_data['token']
        }
        URL_DELETE_ACCOUNT = self.URL_HOST + reverse('user:user-detail', kwargs={'pk': response_data['id']})
        response = requests.delete(URL_DELETE_ACCOUNT, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```


<br>

## 2. Make Field lookup '__exact__in' available in Django

### The meaning of Field lookup '__exact__in' and its usage

The model structure is this.

```python
class Recipe(models.Model):

    ...
    sandwich = models.ForeignKey(
        Sandwich,
        on_delete=models.SET_NULL,
        ...
    )
    bread = models.ForeignKey(
        Bread,
        on_delete=models.SET_NULL,
        ...
    )
    cheese = models.ForeignKey(
        Cheese,
        on_delete=models.SET_NULL,
        ...
    )
    toasting = models.ForeignKey(
        Toasting,
        on_delete=models.SET_NULL,
        ...
    )
    toppings = models.ManyToManyField(
        Toppings,
        ...
    )
    vegetables = models.ManyToManyField(
        Vegetables,
        ...
    )
    sauces = models.ManyToManyField(
        Sauces,
        ...
    )



class Sandwich(models.Model):
    ...

class Bread(models.Model):
    ...

class Cheese(models.Model):
    ...

class Toasting(models.Model):
    ...

class Toppings(models.Model):
    ...

class Vegetables(models.Model):
    ...

class Sauces(models.Model):
    ...

```


In the MySubway app, each recipe object should be unique. In other words, there are not the same recipes.\
If the Recipe model has only Foreignkey relations, the way would be much simpler.\
Just add below code into Recipe model.

```python
    class Meta:
        unique_together = (
            ('sandwich', 'bread', 'cheese', 'toasting', 'toppings', 'vegetables', 'sauces'),
        )
```

However, unfortunately, unique_together cannot be used with a ManyToMany relationship.\
So, the only way is to make Unique Validator and call it in serializer to check the request data for Recipe Create API.

```python
def validate(self, attrs):

    result = recipe_uniqueness_validator(attrs)

    if not result is True:
        raise CustomAPIException(
            ...
        )
    return attrs


def recipe_uniqueness_validator(attrs, **kwargs):

    # Check whether objects that have same Sandwich exist
    recipe_filtered_list = Recipe.objects \
        .filter(sandwich=attrs.get('sandwich'))

    # Check whether objects that have same Bread exist
    recipe_filtered_list = recipe_filtered_list \
        .filter(sandwich=attrs.get('bread'))

    # Check whether objects that have same Cheese exist
    recipe_filtered_list = recipe_filtered_list \
        .filter(sandwich=attrs.get('cheese'))

    # Check whether objects that have same Toppings exist
        ...

    ...
```

For the foreign key relationship, comparing the request data and ForeignKey field is everything we have to do.\
But with ManyToManyFields, it needs Field lookup something like '__exact__in'.\
If we use Field lookup '__in', returned data won't be what we want. For example, Toppings' pk in request data is [1, 3, 5].

`Recipe.objects.filtering(toppings__pk__in=[1, 3, 5]).distinct()`

Filtering above will find not only toppings of [1, 3, 5], but also [1], [1, 3], [1, 3, 5, 6] ...\
So we need to make custom ORM for this specific case.

First, add an annotation with Count() for numbering of each 'toppings'.
'toppings' doesn't mean related_query_name, but the one used in the previous filter.
Filtering 'num_toppings=3' to the annotated queryset will return the data.

```python
Recipe.objects\
        .filter(toppings__pk__in=[1, 3, 5]).distinct() \
        .annotate(num_toppings=Count('toppings', distinct=True)) \
        .filter(num_toppings=3)
```

The returned data is very close but not exactly the answer.
It is something look like [1, 3, 5], [1, 3, 5, 6], [1, 2, 3, 5].
The data contains every toppings we want to find but there are some extra toppings.\
So, the next step is counting out unnecessary data from the result queryset.


```python
Recipe.objects\
        .filter(toppings__pk__in=[1, 3, 5]).distinct() \
        .annotate(num_toppings=Count('toppings', distinct=True)) \
        .filter(num_toppings=3)
        .exclude(pk__in=Recipe.objects
                .annotate(num_toppings=Count('toppings'))
                .filter(num_toppings__gt=3)
        )
```

`
Recipe.objects
        .annotate(num_toppings=Count('toppings'))
        .filter(num_toppings__gt=3)
`

This code will return the queryset that has more than 3 elements like [1, 3, 5, 6], [1, 2, 3, 5].\
Excluding these queryset from the previous queryset will return the exact data we want.

There is another way to do this.
This way use exclude  method twice to get the result.

```python
Recipe.objects\
        .filter(toppings__pk__in=[1, 3, 5]).distinct() \
        .annotate(num_toppings=Count('toppings', distinct=True)) \
        .filter(num_toppings=3)
        .exclude(sauces__in=Sauces.objects.exclude(pk__in=[1, 3, 5])
```

`Sauces.objects.exclude(pk__in=[1, 3, 5]`
The code means data like [1], [1, 3], [1, 5], [3, 5] ...
So the queryset of excluding this data doesn't contain three elements we want to find: 1, 3, 5.\
Excluding these queryset again from the previous queryset will also return the answer.


Here is simple format for '__exact__in' in Django

```python
.filter(<field>__in=[...])
.annotate(num_<field>=Count('<field>', distinct=True)
.filter(num_<field>=len([...]))
.exclude(<field>__in=
        <Model_name_of_field>.objects.exclude(pk__in=[])
```



<br>

## 3. Pass extra data to default JSON API response


Second code review above covered the uniqueness of the Recipe model.
And when the Unique Validator finds the same recipe already existing in the DATABASE, it will return the below response.

```json
{
    "detail": "Same sandwich recipe already exists!",
}
```

But, front-end developers need more than the error message.
They also need the exact number of the duplicate recipe to let user visit the page of the recipe.
So, the response should be something like this.

```json
{
    "detail": "Same sandwich recipe already exists!",
    "pk": 11
}
```

To add that extra pk data to error response message, look at the CustomAPIException first.

```python
from rest_framework import status
from rest_framework.exceptions import APIException

class CustomAPIException(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Invalid input.'
    default_code = 'invalid'

    def __init__(self, status_code=None, detail=None):

        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail
```

This Custom Exception works when it is called with raise statement.


```python
from rest_framework import status

    ...
    raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Same sandwich recipe already exists!',
            )
```

With this Custom Exception, we cannot add extra data to the response message.
In this situation, we can consider Custom Exception Handler.


```python
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    # put 'pk' data to response here

    return response
```

Every exception raised in the app go through Custom Exception Handler.
Therefore, we need to add the data to the response When the exception from Recipe Unique Validator comes to Custom Exception Handler.

To do this, we need to pass 'pk' information to Custom Exception as below.


```python
from rest_framework import status

    ...
    raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Same sandwich recipe already exists!',
                pk=result,
            )
```

Then, Custom Exception get this 'pk' data through keyword argument.


```python
from rest_framework import status
from rest_framework.exceptions import APIException

class CustomAPIException(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Invalid input.'
    default_code = 'invalid'

    pk = None

    def __init__(self, status_code=None, detail=None, pk=None):

        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail

        if pk is not None:
            self.pk = pk

```

Assigning received 'pk' data into self.pk in __init__ method won't pass 'pk' data to Custom Exception Handler.
'pk' should be defined in CustomAPIException as class attribute.
And then, it can be obtained in 'exc' attribute in Custom Exception Handler.


```python
def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    try:
        if exc.pk:
            response.data['pk'] = exc.pk
    finally:
        return response

```

Finally, put 'pk' data into response dict.
'try ~ finally' statement is for raising an error when there is no 'pk' data, which are the case of all other exceptions.

Now, we can get the response with 'pk' data.

```json
{
    "detail": "Same sandwich recipe already exists!",
    "pk": 11
}
```




<br>



<br>

---

<br>

# Issues

### 1. when default djanog-rest-framework page doens't work

### 2.