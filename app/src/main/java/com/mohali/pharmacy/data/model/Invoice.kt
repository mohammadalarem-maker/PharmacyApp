package com.mohali.pharmacy.data.model

data class InvoiceItem(
    val productId  : String = "",
    val productName: String = "",
    val barcode    : String = "",
    val quantity   : Int    = 1,
    val unitPrice  : Double = 0.0,
    val discount   : Double = 0.0,
    val total      : Double = 0.0
)

data class Invoice(
    val id            : String           = "",
    val invoiceNumber : String           = "",
    val customerName  : String           = "",
    val customerPhone : String           = "",
    val items         : List<InvoiceItem>= emptyList(),
    val subtotal      : Double           = 0.0,
    val discount      : Double           = 0.0,
    val tax           : Double           = 0.0,
    val totalAmount   : Double           = 0.0,
    val amountPaid    : Double           = 0.0,
    val change        : Double           = 0.0,
    val paymentMethod : String           = "cash",
    val status        : String           = "paid",
    val notes         : String           = "",
    val createdBy     : String           = "",
    val createdAt     : Long             = System.currentTimeMillis(),
    val updatedAt     : Long             = System.currentTimeMillis()
) {
    fun toMap(): Map<String, Any> = mapOf(
        "id" to id, "invoiceNumber" to invoiceNumber,
        "customerName" to customerName, "customerPhone" to customerPhone,
        "items" to items.map { mapOf(
            "productId" to it.productId, "productName" to it.productName,
            "barcode" to it.barcode, "quantity" to it.quantity,
            "unitPrice" to it.unitPrice, "discount" to it.discount, "total" to it.total
        )},
        "subtotal" to subtotal, "discount" to discount, "tax" to tax,
        "totalAmount" to totalAmount, "amountPaid" to amountPaid, "change" to change,
        "paymentMethod" to paymentMethod, "status" to status, "notes" to notes,
        "createdBy" to createdBy, "createdAt" to createdAt, "updatedAt" to updatedAt
    )
    companion object {
        @Suppress("UNCHECKED_CAST")
        fun fromMap(map: Map<String, Any>): Invoice {
            val its = (map["items"] as? List<Map<String,Any>>)?.map {
                InvoiceItem(
                    productId   = it["productId"]   as? String ?: "",
                    productName = it["productName"] as? String ?: "",
                    barcode     = it["barcode"]     as? String ?: "",
                    quantity    = (it["quantity"]   as? Number)?.toInt()    ?: 1,
                    unitPrice   = (it["unitPrice"]  as? Number)?.toDouble() ?: 0.0,
                    discount    = (it["discount"]   as? Number)?.toDouble() ?: 0.0,
                    total       = (it["total"]      as? Number)?.toDouble() ?: 0.0
                )
            } ?: emptyList()
            return Invoice(
                id            = map["id"]            as? String ?: "",
                invoiceNumber = map["invoiceNumber"] as? String ?: "",
                customerName  = map["customerName"]  as? String ?: "",
                customerPhone = map["customerPhone"] as? String ?: "",
                items         = its,
                subtotal      = (map["subtotal"]     as? Number)?.toDouble() ?: 0.0,
                discount      = (map["discount"]     as? Number)?.toDouble() ?: 0.0,
                tax           = (map["tax"]          as? Number)?.toDouble() ?: 0.0,
                totalAmount   = (map["totalAmount"]  as? Number)?.toDouble() ?: 0.0,
                amountPaid    = (map["amountPaid"]   as? Number)?.toDouble() ?: 0.0,
                change        = (map["change"]       as? Number)?.toDouble() ?: 0.0,
                paymentMethod = map["paymentMethod"] as? String ?: "cash",
                status        = map["status"]        as? String ?: "paid",
                notes         = map["notes"]         as? String ?: "",
                createdBy     = map["createdBy"]     as? String ?: "",
                createdAt     = (map["createdAt"]    as? Number)?.toLong() ?: System.currentTimeMillis(),
                updatedAt     = (map["updatedAt"]    as? Number)?.toLong() ?: System.currentTimeMillis()
            )
        }
    }
}
