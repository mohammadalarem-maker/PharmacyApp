package com.mohali.pharmacy.data.model

data class Product(
    val id           : String  = "",
    val name         : String  = "",
    val barcode      : String  = "",
    val category     : String  = "",
    val price        : Double  = 0.0,
    val purchasePrice: Double  = 0.0,
    val quantity     : Int     = 0,
    val minQuantity  : Int     = 5,
    val imageUrl     : String  = "",
    val description  : String  = "",
    val isActive     : Boolean = true,
    val expiryDate   : String  = "",
    val unit         : String  = "قطعة",
    val manufacturer : String  = "",
    val createdAt    : Long    = System.currentTimeMillis(),
    val updatedAt    : Long    = System.currentTimeMillis()
) {
    fun toMap(): Map<String, Any> = mapOf(
        "id" to id, "name" to name, "barcode" to barcode,
        "category" to category, "price" to price,
        "purchasePrice" to purchasePrice, "quantity" to quantity,
        "minQuantity" to minQuantity, "imageUrl" to imageUrl,
        "description" to description, "isActive" to isActive,
        "expiryDate" to expiryDate, "unit" to unit,
        "manufacturer" to manufacturer, "createdAt" to createdAt,
        "updatedAt" to updatedAt
    )
    companion object {
        fun fromMap(map: Map<String, Any>): Product = Product(
            id            = map["id"]            as? String  ?: "",
            name          = map["name"]          as? String  ?: "",
            barcode       = map["barcode"]       as? String  ?: "",
            category      = map["category"]      as? String  ?: "",
            price         = (map["price"]         as? Number)?.toDouble() ?: 0.0,
            purchasePrice = (map["purchasePrice"] as? Number)?.toDouble() ?: 0.0,
            quantity      = (map["quantity"]      as? Number)?.toInt()    ?: 0,
            minQuantity   = (map["minQuantity"]   as? Number)?.toInt()    ?: 5,
            imageUrl      = map["imageUrl"]      as? String  ?: "",
            description   = map["description"]   as? String  ?: "",
            isActive      = map["isActive"]      as? Boolean ?: true,
            expiryDate    = map["expiryDate"]    as? String  ?: "",
            unit          = map["unit"]          as? String  ?: "قطعة",
            manufacturer  = map["manufacturer"]  as? String  ?: "",
            createdAt     = (map["createdAt"]     as? Number)?.toLong() ?: System.currentTimeMillis(),
            updatedAt     = (map["updatedAt"]     as? Number)?.toLong() ?: System.currentTimeMillis()
        )
    }
}

data class CartItem(
    val product : Product,
    var quantity: Int    = 1,
    var discount: Double = 0.0
) {
    val total: Double get() = (product.price * quantity) - discount
}
