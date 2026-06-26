package com.mohali.pharmacy.data.repository

import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import com.mohali.pharmacy.data.model.Invoice
import kotlinx.coroutines.tasks.await
import java.text.SimpleDateFormat
import java.util.*
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class InvoiceRepository @Inject constructor(private val db: FirebaseFirestore) {
    private val col = db.collection("invoices")

    suspend fun getAll(): List<Invoice> = col
        .orderBy("createdAt", Query.Direction.DESCENDING).get().await().documents
        .mapNotNull { d -> d.data?.let { Invoice.fromMap(it.also { m -> m["id"] = d.id }) } }

    suspend fun getById(id: String): Invoice? = col.document(id).get().await()
        .let { d -> d.data?.let { Invoice.fromMap(it.also { m -> m["id"] = d.id }) } }

    suspend fun getTodaySales(): Double {
        val cal = Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, 0); set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0); set(Calendar.MILLISECOND, 0)
        }
        return col.whereGreaterThanOrEqualTo("createdAt", cal.timeInMillis)
            .get().await().documents
            .mapNotNull { d -> d.data?.let { Invoice.fromMap(it.also { m -> m["id"] = d.id }) } }
            .sumOf { it.totalAmount }
    }

    suspend fun create(inv: Invoice): String {
        val num = "INV-${SimpleDateFormat("yyyyMMdd", Locale.getDefault()).format(Date())}-${(1000..9999).random()}"
        val ref = col.add(inv.copy(invoiceNumber = num).toMap()).await()
        col.document(ref.id).update("id", ref.id).await()
        return ref.id
    }

    suspend fun update(inv: Invoice) {
        col.document(inv.id).set(inv.copy(updatedAt = System.currentTimeMillis()).toMap()).await()
    }

    suspend fun delete(id: String) { col.document(id).delete().await() }
}
