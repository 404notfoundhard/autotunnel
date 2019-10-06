nginx
=========

Installs and configures nginx.

Requirements
------------

None.

Role Variables
--------------

```yml
postgresql_admin_user:          postgres
postgresql_version:             9.5
postgresql_ext_postgis_version: 2.2
postgresql_port:                5432
postgresql_db_name:             site
postgresql_db_owner:            vagrant
postgresql_db_password:         vagrant

postgresql_encoding: 'UTF-8'
postgresql_locale_parts:
  - 'en_US' # Locale
  - 'UTF-8' # Encoding
postgresql_locale: "{{ postgresql_locale_parts | join('.') }}"

postgresql_extensions:
  - hstore
  - postgis

postgresql_users:
  - { username: '{{ postgresql_db_owner }}', password: '{{ postgresql_db_password }}' }
```

Dependencies
------------

```
bearandgiraffe.base
```

Example Playbook
----------------

```yml
- hosts: servers
  roles:
    - { role: bearandgiraffe.postgresql, postgresql_db_name: 'my_database_name' }
```

License
-------

The Unlicense (see LICENSE)

Author Information
------------------

Youssef Chaker (@ychaker) from Bear & Giraffe LLC (@bearandgiraffe).
