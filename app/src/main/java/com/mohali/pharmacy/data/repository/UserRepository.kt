package com.mohali.pharmacy.data.repository

import com.google.firebase.FirebaseApp
import com.google.firebase.FirebaseOptions
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.mohali.pharmacy.data.model.AppUser
import kotlinx.coroutines.tasks.await
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class UserRepository @Inject constructor(
    private val auth: FirebaseAuth,
    private val db  : FirebaseFirestore
) {
    private val col = db.collection("users")

    suspend fun getAll(): List<AppUser> = col.get().await().documents
        .mapNotNull { d -> d.data?.let { AppUser.fromMap(it.also { m -> m["uid"] = d.id }) } }

    suspend fun create(name: String, email: String, pass: String,
                       role: String, perms: List<String>): Result<AppUser> = try {
        // Use secondary app instance to avoid displacing admin session
        val appName = "secondary_auth"
        val secondaryApp = try {
            FirebaseApp.getInstance(appName)
        } catch (e: Exception) {
            FirebaseApp.initializeApp(
                FirebaseApp.getInstance().applicationContext,
                FirebaseApp.getInstance().options,
                appName
            )!!
        }
        val secAuth = FirebaseAuth.getInstance(secondaryApp)
        val r = secAuth.createUserWithEmailAndPassword(email, pass).await()
        val uid = r.user?.uid ?: error("فشل إنشاء المستخدم")
        secAuth.signOut()
        val u = AppUser(uid = uid, name = name, email = email,
                        role = role, permissions = perms, isActive = true)
        col.document(uid).set(u.toMap()).await()
        Result.success(u)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun update(u: AppUser) { col.document(u.uid).set(u.toMap()).await() }

    suspend fun delete(uid: String) { col.document(uid).delete().await() }

    suspend fun setPermissions(uid: String, perms: List<String>) {
        col.document(uid).update("permissions", perms).await()
    }

    suspend fun setActive(uid: String, active: Boolean) {
        col.document(uid).update("isActive", active).await()
    }
}
