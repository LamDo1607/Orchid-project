# PRJ3.3 Orchid



## How to run

### Import default database

Create database by cmd
```
mongo
```

```
use orchid
```


```
db.createUser(
  {
    user: "vohungvi",
    pwd: "viscomsolution",
    roles: [ { role: "readWrite", db: "orchid" } ]
  })

```

Import database: run file **restore_db.bat**

