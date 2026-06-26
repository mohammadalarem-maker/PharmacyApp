package com.mohali.pharmacy.data.model

data class AppUser(
    val uid        : String       = "",
    val name       : String       = "",
    val email      : String       = "",
    val phone      : String       = "",
    val role       : String       = "cashier",
    val permissions: List<String> = emptyList(),
    val isActive   : Boolean      = true,
    val createdAt  : Long         = System.currentTimeMillis()
) {
    fun toMap(): Map<String, Any> = mapOf(
        "uid" to uid, "name" to name, "email" to email, "phone" to phone,
        "role" to role, "permissions" to permissions,
        "isActive" to isActive, "createdAt" to createdAt
    )
    companion object {
        val ALL_PERMISSIONS = listOf(
            "view_inventory","manage_inventory","create_sale",
            "view_invoices","manage_invoices","view_reports","manage_users"
        )
        val PERMISSION_LABELS = mapOf(
            "view_inventory"    to "عرض المخزون",
            "manage_inventory"  to "إدارة المخزون",
            "create_sale"       to "إنشاء مبيعات",
            "view_invoices"     to "عرض الفواتير",
            "manage_invoices"   to "إدارة الفواتير",
            "view_reports"      to "عرض التقارير",
            "manage_users"      to "إدارة المستخدمين"
        )
        val ROLE_LABELS = mapOf(
            "admin" to "مدير النظام","pharmacist" to "صيدلاني",
            "manager" to "مدير","cashier" to "كاشير"
        )
        @Suppress("UNCHECKED_CAST")
        fun fromMap(map: Map<String, Any>): AppUser = AppUser(
            uid         = map["uid"]   as? String ?: "",
            name        = map["name"]  as? String ?: "",
            email       = map["email"] as? String ?: "",
            phone       = map["phone"] as? String ?: "",
            role        = map["role"]  as? String ?: "cashier",
            permissions = (map["permissions"] as? List<String>) ?: emptyList(),
            isActive    = map["isActive"] as? Boolean ?: true,
            createdAt   = (map["createdAt"] as? Number)?.toLong() ?: System.currentTimeMillis()
        )
    }
}
