# django-boosmap

## Starting
_These instructions will allow you to install the library in your python project._

### Current features

-   Get default payload.
-   Create shipping.

### Pre-requisitos

-   Python >= 3.7
-   Django >= 3
-   requests >= 2
***
## Installation

1. To get the latest stable release from PyPi:
```
pip install django-boosmap
```
or

2. From a build
```
git clone https://gitlab.com/linets/ecommerce/oms/integrations/django-boosmap
```

```
cd {{project}}
```

```
python setup.py sdist
```
and, install in your project django
```
pip install {{path}}/django-boosmap/dist/{{tar.gz file}}
```

3. Settings in django project

```
DJANGO_BOOSMAP = {
    'BOOSMAP': {
        'BASE_URL': '<BOOSMAP_BASE_URL>',
        'TOKEN': '<BOOSMAP_TOKEN>',
        'SERVICE': '<BOOSMAP_SERVICE>',
        'START_TIME': '<BOOSMAP_START_TIME>',
        'END_TIME': '<BOOSMAP_END_TIME>',
    },
    'SENDER': {
        'CD_NAME': '<BOOSMAP_CD_NAME>',
        'CD_ADDRESS': '<BOOSMAP_CD_ADDRESS>',
        'CD_COMMUNE': '<BOOSMAP_CD_COMMUNE>',
        'CD_LOCATION_ID': '<BOOSMAP_CD_LOCATION_ID>',
    }
}
```

## Usage

1. Create instance to be sent
    ```
    import json
    from types import SimpleNamespace

    dict_ = {
        'reference': '99999',
        'delivery_date': '2018-12-06 13:00:00'
        'created_at': '12/12/21',
        'shipping_date': '12/12/21',
        'expiration_date': '26/12/21'
        'tracking_code': '6075620-1',
        'transport_guide_number': '1121632479536-01-1',
        'purchase_number': 'CLV0048146676851-1',
        'items': [
            {
                'code': 'SKU1234',
                'name': 'POLOS',
                'price': '2500',
                'qty': '2'
            },
            {
                'code': 'SKU12345',
                'name': 'SHORT',
                'price': '1500',
                'qty': '1'
            }
        ]
        'customer': {
            'first_name': 'Marcos',
            'last_name': 'Sac',
            'full_name': 'Marcos Sac',
            'phone': '932932932',
            'email': 'test@gmail.com',
            'rut': '16936195-9'
        },
        'address': {
            'street': 'ALEJANDRO VENEGAS CADIZ',
            'number': '513',
            'unit': 'DEPTO 6A',
            'full_address': 'ALEJANDRO VENEGAS CADIZ 513 DEPTO 6A'
        },
        'commune': {
            'name': 'Aisen',
            'code': '',
            'zone_code': '11201',
            'zone_post': 'WPA',
        },
        'location': {
            'code': 'MONTANDON',
            'name': 'MNN',
        },
        'region': {
            'name': 'Aysén del General Carlos Ibáñez del Campo',
            'code': '11',
            'iso_code': 'CL-XI',
        }
    }

    instance = json.loads(json.dumps(dict_), object_hook=lambda attr: SimpleNamespace(**attr))
    ```

2. Get default payload:
```
from boosmap.handler import BoosmapHandler

handler = BoosmapHandler()
default_data = handler.get_default_payload(<instance>)
```

3. Create shipping:
```
from boosmap.handler import BoosmapHandler

handler = BoosmapHandler()
default_data = handler.create_shipping(<default_data>)
```

4. Get events:
```
from boosmap.handler import BoosmapHandler

handler = BoosmapHandler()

raw_data = {
    'tracking_number': 999999,
    'status': 'Entregado',
    'events': [{
        'city': 'Santiago'
        'state': 'RM',
        'description': 'Llego al almacén',
        'date': '12/12/2021'
    }]
}
response = handler.get_events(raw_data)

Output:
[{
    'city': 'Santiago'
    'state': 'RM',
    'description': 'Llego al almacén',
    'date': '12/12/2021'
}]
```

5. Get status and if "is_delivered":
```
from boosmap.handler import BoosmapHandler

handler = BoosmapHandler()

raw_data = {
    'tracking_number': 999999,
    'status': 'Entregado',
    'events': [{
        'city': 'Santiago'
        'state': 'RM',
        'description': 'Llego al almacén',
        'date': '12/12/2021'
    }]
}
response = handler.get_status(raw_data)

Output:
('Entregado', True)
```
