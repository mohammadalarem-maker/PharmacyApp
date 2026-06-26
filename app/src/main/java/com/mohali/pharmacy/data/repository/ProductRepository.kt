package com.mohali.pharmacy.data.repository

import android.net.Uri
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import com.mohali.pharmacy.data.model.Product
import kotlinx.coroutines.tasks.await
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ProductRepository @Inject constructor(
    private val db     : FirebaseFirestore,
    private val storage: FirebaseStorage
) {
    private val col = db.collection("products")

    suspend fun getAll(): List<Product> = col.get().await().documents
        .mapNotNull { d -> d.data?.let { Product.fromMap(it.also { m -> m["id"] = d.id }) } }

    suspend fun getActive(): List<Product> = col.whereEqualTo("isActive", true)
        .get().await().documents
        .mapNotNull { d -> d.data?.let { Product.fromMap(it.also { m -> m["id"] = d.id }) } }

    suspend fun getByBarcode(barcode: String): Product? =
        col.whereEqualTo("barcode", barcode).limit(1).get().await()
            .documents.firstOrNull()?.let { d ->
                d.data?.let { Product.fromMap(it.also { m -> m["id"] = d.id }) }
            }

    suspend fun add(p: Product): String {
        val ref = col.add(p.toMap()).await()
        col.document(ref.id).update("id", ref.id).await()
        return ref.id
    }

    suspend fun update(p: Product) {
        col.document(p.id).set(p.copy(updatedAt = System.currentTimeMillis()).toMap()).await()
    }

    suspend fun delete(id: String) { col.document(id).delete().await() }

    suspend fun updateQty(id: String, qty: Int) {
        col.document(id).update("quantity", qty, "updatedAt", System.currentTimeMillis()).await()
    }

    suspend fun uploadImage(uri: Uri, productId: String): String {
        val ref = storage.reference.child("products/$productId.jpg")
        ref.putFile(uri).await()
        return ref.downloadUrl.await().toString()
    }

    suspend fun getLowStock(): List<Product> =
        col.whereEqualTo("isActive", true).get().await().documents
            .mapNotNull { d -> d.data?.let { Product.fromMap(it.also { m -> m["id"] = d.id }) } }
            .filter { it.quantity <= it.minQuantity }
}
