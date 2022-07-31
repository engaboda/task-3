## [User](integeration/models.py)

## [Keycloak](integeration/keycloak/)

## RUN

`docker-compose up --build`


## Test coverage
```
Name                             Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------
integeration/__init__.py             0      0      0      0   100%
integeration/admin.py                1      0      0      0   100%
integeration/apps.py                 4      0      2      0   100%
integeration/authentication.py      33      5      6      1    85%   24-25, 28, 37-38
integeration/constants.py            2      0      0      0   100%
integeration/jwt_views.py           27      3      6      1    88%   29-30, 38
integeration/keycloak/token.py      65     19     16      2    72%   40-55, 93-95, 102-103, 115-117
integeration/keycloak/user.py       51     15      6      1    68%   43-60, 77-79, 88-89
integeration/manager.py             21      6      8      3    69%   8, 15-17, 24, 26
integeration/models.py               9      1      2      0    91%   20
integeration/permissions.py         12      0      8      0   100%
integeration/serializers.py          4      0      2      0   100%
integeration/tests.py               97      4     10      0    96%   17, 21, 36, 40
integeration/urls.py                 4      0      0      0   100%
integeration/viewsets.py            14      0      4      0   100%
keycloak_drf/__init__.py             0      0      0      0   100%
keycloak_drf/asgi.py                 4      4      0      0     0%   10-16
keycloak_drf/settings.py            43      0      2      1    98%   26->41
keycloak_drf/urls.py                 4      0      0      0   100%
keycloak_drf/wsgi.py                 4      4      0      0     0%   10-16
manage.py                           12      2      2      1    79%   12-13, 21->exit
requirments.py                       7      7      0      0     0%   1-7
----------------------------------------------------------------------------
TOTAL                              418     70     74     10    83%

```