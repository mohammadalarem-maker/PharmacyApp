package com.mohali.pharmacy.navigation

sealed class Screen(val route: String) {
    object Login         : Screen("login")
    object Main          : Screen("main")
    object AddProduct    : Screen("add_product?barcode={barcode}") {
        fun route(bc: String = "") = "add_product?barcode=$bc"
    }
    object EditProduct   : Screen("edit_product/{productId}") {
        fun route(id: String) = "edit_product/$id"
    }
    object InvoiceDetail : Screen("invoice_detail/{invoiceId}") {
        fun route(id: String) = "invoice_detail/$id"
    }
    object CreateInvoice : Screen("create_invoice")
    object AddEditUser   : Screen("add_edit_user?uid={uid}") {
        fun route(uid: String = "") = "add_edit_user?uid=$uid"
    }
}
