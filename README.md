DIASPO API
====================

# Datos importantes

## Tipos de Proyectos/Negocios
```
business_type:
    1- Personales
    2- Generales
    3- Deudas
```

## Monedas
```
1 | Dolar | $ | USD
2 | Nuevo Sol | S/ | PEN
3 | Bolivar | Bs. | VEF
4 | Peso Colombiano | $ | COP
```

# Crear usuario
---

  Para crear un nuevo usuario en el sistema.

## URL

`/user`

## Method

`POST`

## Headers Params
`none`

## Body Params
```

`email=[string]` **required**
`password=[string]` **required**
`display_name=[string]` **required**

```
## Sample Call:

```
{
  "email":"fernando.zmorales@gmail.com",
  "password":"abc123",
  "display_name":"Fernando Morales"
}
```

## Success Response:

**Code:** 200
**Content:** 

```
{
  "msg": "Usuario creado exitosamente",
  "success": "true",
  "user": {
      "display_name": "Fernando Fernando",
      "email": "fernando.zmorales2@gmail.com",
      "photo_url": null,
      "uid": "QkN6iypCwuOwrs7dxgYnPlZNImm2"
}
```

# Obtener datos usuario
---

  Para obtener los datos de un usuario ya logueado. Se necesita enviar el token de Firebase en el Header.

## URL

`/user`

## Method

`GET`

## Headers Params
`x-access-token`

## Body Params
`none`


## Success Response:

**Code:** 200
**Content:** 

```
{
  "msg": "",
  "success": "true",
  "user": {
      "id": 3,
      "email": "fernando.zmorales2@gmail.com",
      "display_name": 'Fernando Morales',
      "role": "1"
}
```


# Obtener datos iniciales
---

  Los datos iniciales que se muestran en el home, incluye el ultimo valor que se agregó movimiento para que se seleccione por defecto, si se encuentra el valor "is_last_selected" como activo (1).

## URL

`/home`

## Method

`GET`

## Headers Params
`x-access-token`

## Body Params
`none`

## Success Response:

**Code:** 200
**Content:** 

```

{
  "summaries_bussines": [
    {
      "accounts": [
        {
          "creator_id": 3, 
          "currency_abbr": "S/", 
          "currency_code": "PEN", 
          "currency_id": 2, 
          "id": 1, 
          "is_last_sected": 0, 
          "name": "Efectivo Soles", 
          "total_amount": 35.0
        }, 
        {
          "creator_id": 3, 
          "currency_abbr": "$", 
          "currency_code": "USD", 
          "currency_id": 1, 
          "id": 1, 
          "is_last_sected": 1, 
          "name": "Efectivo Dolares", 
          "total_amount": 100.0
        }
      ], 
      "business_type": 1, 
      "creator_id": 3, 
      "id": 1, 
      "is_favorite": 0, 
      "is_last_sected": 0, 
      "members": [], 
      "name": "Cuenta personal de Pepito"
    }, 
    {
      "accounts": [
        {
          "creator_id": 3, 
          "currency_abbr": "S/", 
          "currency_code": "PEN", 
          "currency_id": 2, 
          "id": 3, 
          "is_last_sected": 0, 
          "name": "Efectivo Soles", 
          "total_amount": 10.0
        }, 
        {
          "creator_id": 3, 
          "currency_abbr": "$", 
          "currency_code": "USD", 
          "currency_id": 1, 
          "id": 4, 
          "is_last_sected": 0, 
          "name": "Efectivo Dolares", 
          "total_amount": 12.0
        }
      ], 
      "business_type": 2, 
      "creator_id": 3, 
      "id": 1, 
      "is_favorite": 0, 
      "is_last_sected": 0, 
      "members": [
        {
          "email": "fernando.zmorales@gmail.com", 
          "id": 3, 
          "display_name": "Fernando Morales"
        }, 
        {
          "email": "carlomurga@gmail.com", 
          "id": 4, 
          "display_name": "Carlo Murga"
        }
      ], 
      "name": "Diaspora Proyect"
    }
  ]
}

```

# Crear Proyecto o Business
---

  Para crear un nuevo proyecto business o cuenta asociado a un usuario

## URL

`/business`

## Method

`POST`

## Headers Params
`x-access-token`

## Body Params
```

`name=[string]` **required**
`bussiness_type=[int]` **required**
`is_favorite=[int]` 

```
## Sample Call:

```
{
  "is_favorite":0,
  "bussiness_type":2,
  "name":"Diaspora proyect"
}
```

## Success Response:

**Code:** 200
**Content:** 

```
{
  "msg": "Business creado correctamente",
  "success": "true"
}
```

# Crear Monedero o Money Bucket 
---

  Para crear un nuevo proyecto business o cuenta asociado a un usuario

## URL

`/account`

## Method

`POST`

## Headers Params
`x-access-token`

## Body Params
```

`name=[string]` **required**
`business_id=[int]` **required**
`currency_id=[int]` **required**
`initial_amount=[float]` (default 0)

```
## Sample Call:

```
{
  "initial_amount":0,
  "currency_id":2,
  "business_id":3,
  "name":"Efectivo Soles"
}
```

## Success Response:

**Code:** 200
**Content:** 

```
{
  "msg": "Cuenta creada correctamente",
  "success": "true"
}
```


# Crear Movimiento 
---

  Para crear movimiento bien sea negativo o positivo

## URL

`/movement`

## Method

`POST`

## Headers Params
`x-access-token`

## Body Params
```

`account_id=[int]` **required**
`amount=[float]` **required**
`subject=[string]`

```
## Sample Call:

```
{
  "account_id":3,
  "amount":-30.00,
  "subject":"Gasto de compra de panes"
}
```

## Success Response:

**Code:** 200
**Content:** 

```
{
  "msg": "Movimiento registrado correctamente",
  "success": "true"
}
```

# Ver detalle de Cuenta o  Moneybucket
---

  Para crear un nueva Cuenta o Moneybucket asociada a un usuario

## URL

`/account/id`

## Method

`GET`

## Headers Params
`x-access-token`


## Sample Call:

```
/account/15
```

## Success Response:

**Code:** 200
**Content:** 

```
{
  "msg": "Cuenta creada correctamente",
  "success": "true"
}
```


# Ver detalle de Proyecto o Negocio
---

  Para crear un nuevo proyecto business asociada a un usuario

## URL

`/business/id`

## Method

`GET`

## Headers Params
`x-access-token`


## Sample Call:

```
/business/3
```

## Success Response:

**Code:** 200
**Content:** 

```
{
  "msg": "Cuenta creada correctamente",
  "success": "true"
}
```


