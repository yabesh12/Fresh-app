# DB Design

### Tables Available

- Product type
- Product Category
- Product
- Price Groups
- ProductByPriceGroup
- Route
- Shops
- Orders
- orderItems
- credit
- credit limits
- request 
- request Items
- Payments(either credit or Debit data Transactions)
- Reconcilation
- Reconcilation items
- distributor 
- InventorybasedonDistributor



```
 ProductType
   - title
   - is_credit_available
   - units (kg, package, case, dozon)
   - is_active
   - tax
```

```
Product Category
    - name
    - slug
    - is_active
```
```
Product
    - name
    - category
    - product type
    - base price
    - MRP price
    - selling price
    - sku
    - slug
    - unit
    - weight
    - is_active
    - self life

```

```
Route 
    - name
    - Geolocation
    - Description
    - Start
    - End
    - Pincodes
```

```
Shop Category
    - name
    - slug
    - is_active
```

```
Shop
    - name
    - category
    - slug
    - is_active
    - geolocation
    - place
    - address
    - gst number
    - phone number
    - wallet
    - total credit limit
    - total credit
    - is chain
    - route
    - is parent
```
```
Order
    - id (pk)
    - total
    - is paid
    - paid date
    - status
    - is active
```
```
Order Item
    - order
    - product
    - quantity
    - price
```

```
Credit
    - amount
    - shop
    - category
    - limit
```
```
Request
    - sales person
    - shop
    - status
    - requested date
    - due date (date & time)
    - is active

```

```
Request Items
    - request
    - product
    - quantity
```

```
Payments
    - order
    - credit status
    - debit status
    - shop
    - is_closed
    - distributor
```
```
Reconcilation
    - shop
    - reconcilation date
    - is active
    - status
    - distributor
    - reconcilation_type 
```

```
Reconciliation Items
    - reconcilation
    - product
    - quantity
    - price
```
```
Distributor
    - name
    - age
    - vehicle number
    - phone_number
    - address
    - permanent_route
    - temporary_route
    - is_active
```
```
InventoryBased On Distributor
   - distributor
   - product
   - stock
```
```
InventoryLog
   - Inventory 
   - distributor
   - product
   - stock
   - date   
```