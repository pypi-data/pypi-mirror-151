## Sqlalchemy Module V0.3.1

[Fachada](https://refactoring.guru/es/design-patterns/facade) de la libreria Sqlalchemy 1.4.x

| Properties         | Requerido          | Valor por defecto | Descripción                                                                                                                                                             |
|--------------------|--------------------|:-----------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| url_connection     | :heavy_check_mark: |       -           | Url de conexión de la base de datos                                                                                                                                     |
| path_module_schema | :heavy_check_mark: |       -           | Paquete de python donde se almacenaran todos las clases python que representan las tablas de base de datos                                                              |
| ddl_auto           | :heavy_check_mark: |       -           | Atributo que dependiendo de una valores especificos actuan sobre el comportamiento de la base de datos cuando arranca la aplicación                                     |


![diagramainterfaces](docs/interfaces.png)
![diagrama](docs/diagrama.png)
## QuickStart

En el momento que se importa el módulo "postgresql_db" se ejecuta la funcion "load_declarative_models()" esta funcion es
la encargada de gestionar la creacion de la base de datos, por defecto usa la configuración del archivo properties.ini.

### propertie ddl_auto

Dentro del archivo configuracion se puede definir un parametro "ddl_auto" que en funcion del valor actua de diferente
manera contra la base de datos

```properties
[BD_CORE]
db_ip=172.17.0.2
db_port=5432
db_user=postgres
db_password=mysecretpassword
db_name=sqlalchemy
url_connection=postgresql+psycopg2://%(db_user)s:%(db_password)s@%(db_ip)s:%(db_port)s/%(db_name)s
path_module_schema=models
ddl_auto=create

```

#### ddl_auto=create

Usando los modelos representados con clases de python genera las tablas automaticamente cuando se importa el módulo
"postgresql_db", en el caso de que se realicen modificaciones de las tablas ya existentes, no se actualizara. 
Para este caso se debe borrar manualmente la tabla para que se cree nuevamente

#### ddl_auto=drop_create

Esta opcion brinda la opción de borrar todas las tables que esten representadas en los modelos y la vuelve a generar.
Si existe una tabla y no esté representada en el modelo por algun cambio esta tabla no se borrara.

#### ddl_auto=*any

Cualquier otro valor no tendra ningun efecto.

#### ddl_auto (Manual)

Para casos como test u otros casos en particular, se puede usar manualmente la funcion para decidir en que momento
se debe crear o reiniciar las tablas de la base de datos

###### properties.ini
```properties
[BD_CORE]
db_ip = 172.17.0.2
db_port = 5432
db_user = postgres
db_password = mysecretpassword
db_name = sqlalchemy
url_connection = postgresql+psycopg2://%(db_user)s:%(db_password)s@%(db_ip)s:%(db_port)s/%(db_name)s

path_module_schema=models
ddl_auto=null
```
###### main.py
```python
from postgresql_db import load_declarative_models

if __name__ == '__main__':    
    # Creara las tablas
    load_declarative_models(ddl_auto='creative')
    # Recreara las tablas
    load_declarative_models(ddl_auto='drop_create')

```

