# Authorizer

## Описание

Утилитарный пакет, содержащий в себе интеграционный модуль с сервисом Authorizer.

## Установка библиотеки

```
pip install vtb-authorizer-utils
```

с инструментами тестирования и проверки качества кода

```
pip install vtb-authorizer-utils[test]

pip install -e '.[test]'
```

## Быстрый старт

### AuthorizerGateway

Создание объекта AuthorizerGateway от имени сервисной учетной записи. Некоторые сервисы требуют вызов от имени учетной
записи портала.

```python
from dotenv import load_dotenv
from envparse import env
from vtb_authorizer_utils.gateway import AuthorizerGateway
from vtb_http_interaction.http_utils import make_environ_keycloak_config

load_dotenv()

keycloak_config = make_environ_keycloak_config()

authorizer_base_url = env.str('AUTHORIZER_BASE_URL')
redis_url = env.str('REDIS_URL')

gateway = AuthorizerGateway(authorizer_base_url, keycloak_config, redis_url)
```

Создание объекта AuthorizerGateway от имени учетной записи портала (требуется access_token от keycloak)

```python
from dotenv import load_dotenv
from envparse import env
from vtb_authorizer_utils.gateway import AuthorizerGateway
from vtb_http_interaction.keycloak_gateway import KeycloakGateway, UserCredentials
from vtb_http_interaction.http_utils import make_environ_keycloak_config

load_dotenv()

keycloak_config = make_environ_keycloak_config()

user_credentials = UserCredentials(
    username=env.str('KEYCLOAK_TEST_USER_NAME'),
    password=env.str('KEYCLOAK_TEST_USER_PASSWORD')
)

authorizer_base_url = env.str('AUTHORIZER_BASE_URL')
redis_url = env.str('REDIS_URL')

with KeycloakGateway(keycloak_config) as gateway:
    gateway.obtain_token(user_credentials, grant_type=("password",))
    access_token = gateway.access_token

gateway = AuthorizerGateway(authorizer_base_url, access_token=access_token)
```

### Работа с организациями

Получение списка организаций

```
organizations = await gateway.get_organizations()
```

Получение организации по name

```
organization = await gateway.get_organization(name)
```

Получение проектов организации

```
projects = await user_gateway.get_organization_projects(name)
```

Получение потомков организации

```
children = await user_gateway.get_organization_children(name)
```

### Работа с папками

Получение папки

```
folder = await user_gateway.get_folder(name)
```

Получение потомков папки

```
folder = await user_gateway.get_folder_children(name)
```

Получение предков папки

```
folder = await user_gateway.get_folder_ancestors(name)
```

### Работа с проектами

Получение проекта по name

```
project = await user_gateway.get_project(name)
```

Получение предков проекта

```
project = await user_gateway.get_project_ancestors(name)
```

### Работа с пользователями

Получение списка пользователей

```
users = await gateway.get_users(page=1, per_page=10, firstname="иванов", lastname="иванов")
```

Получение пользователя по его идентификатору

```
user = await gateway.get_user(users[0].remote_id)
```

### Прочее

Загрузка конфигурации ресурсных типов и правил для сервиса в виде словаря

```
with open(file, encoding="utf-8") as json_file:
    cfg = json.load(json_file)
    service, resource_types, resource_rules = await import_service_from_dict(gateway, cfg)
```

# Построение схемы импорта сервиса в Authorizer

API делится на 3 типа на основе ролевой модели:

- internal - используется для межсервисного взаимодействия только через системные учетные записи(СУЗ). Вызовы под СУЗ
  пользователей запрещены. Контекст не проверяется.
- admin - предназначен для доступов вне контекста. Это например, конструктор продуктов. Для него доступы выделяются
  независимо от оргструктуры и подразумевается ролевая модель без учёта контекста. Отличие от internal в том, что в этот
  тип API можно вызвать под пользовательским токеном.
- public - пользователи, сервисные аккаунты(в том числе пользовательские). Если есть контекст в URL, то он будет
  проверяться на наличие доступа.

Используемые типы контекста

```
class ContextType(enum.Enum):
    """ Типы контекста """
    ORGANIZATIONS = 'Organizations'  # Контекст организации
    FOLDERS = 'Folders'  # Контекст папки
    PROJECTS = 'Projects'  # Контекст проекта
    DEFAULT = 'Default'  # Без контекста
```

## Добавление описания сервиса

Добавление информации о сервисе для импорта в Authorizer, функция, которая должна быть вызвана до обработки декораторов,
например в самом верху файла views.py

- name: имя сервиса
- title: наименование
- url: базовый URL сервиса, который используется для доступа через шлюз
- description: описание

```
authorizer_service(name='tags-service',
                   title='Сервис тегов',
                   description='',
                   url=settings.KONG_TAG_SERVICE_URL)
```

## Добавление описания ресурсного типа

Декоратор, который применяется к классу, реализующего методы REST API.

- service: имя сервиса, к которому будут привязаны правила
- name: имя ресурсного типа
- title: наименование
- description: описание
- base_url_pattern: базовый URL, если указан, то происходит дополнительная регистрация стандартных REST методов
- default_context_types: контексты доступа, которые указывается у стандартных REST методов. Доступные варианты см. "
  Используемые типы контекста"
- default_access_type: тип доступа, который указывается у стандартных REST методов, по умолчанию 'public'
- url_pattern_postfix: постфикс базового URL, по умолчанию '/'

```
ALL_CONTEXT_TYPES = {ContextType.ORGANIZATIONS, ContextType.FOLDERS, ContextType.PROJECTS}

@authorizer_resource_type(service='tags-service', name='tags', title='Теги', description='',
                          base_url_pattern='/api/v1/{context_type}/{id}/tags/',
                          default_context_types=ALL_CONTEXT_TYPES)
class TagViewSet(AuthenticationViewMixin, viewsets.ModelViewSet):
    pass
```

## Добавление информации о ресурсном правиле для импорта в Authorizer

Добавление описания ресурсного правила. Декоратор, который применяется к методу классу, реализующего метод REST API

- http_method: HTTP метод: get, post, put, patch, delete
- url_pattern: шаблон URL, например, /api/v1/{context_type}/{id}/tags/*/, где
    - {context_type} - в случае указания контекста в context_types, параметр будет заменен на 'organizations', 'folders'
      или 'projects'. Будет создано столько правил, сколько указано контекстов в параметре context_types
    - {id} - служебный параметр, который обрабатывается авторайзером
    - "*" указывает, что в этом месте может быть любое значение, например идентификатор сущности
- access_type: тип доступа. Возможные варианты internal, admin, public
- operation_name: имя операции
- action_code: уникальный код действия, который используется для заполнения поля "ДЕЙСТВИЯ" у сервиса
- context_types: контексты доступа. Доступные варианты 'organizations', 'folders', 'projects'

```
ALL_CONTEXT_TYPES = {ContextType.ORGANIZATIONS, ContextType.FOLDERS, ContextType.PROJECTS}

@authorizer_resource_rule(context_types=ALL_CONTEXT_TYPES,
                              http_method='DELETE',
                              url_pattern='/api/v1/{context_type}/{id}/tags/*/inventory-tags/',
                              access_type='public',
                              operation_name='Delete inventory-tags')
def inventory_tags(self, request, *args, **kwargs): 
    pass
```

## Автогенерация правил

В случае, если пометить класс декоратором authorizer_resource_type, указав у него base_url_pattern, автоматически будут
сгенерированы правила авторайзера для REST API по умолчанию:

1. для методов класса get, post, put, patch, delete, create, retrieve, update, list, destroy
2. для методов, помеченных декоратором django `@action`

```
ALL_CONTEXT_TYPES = {ContextType.ORGANIZATIONS, ContextType.FOLDERS, ContextType.PROJECTS}

@authorizer_resource_type(service='tags-service', name='tags', title='Теги', description='',
                          base_url_pattern='/api/v1/{context_type}/{id}/tags/',
                          default_context_types=ALL_CONTEXT_TYPES)
```