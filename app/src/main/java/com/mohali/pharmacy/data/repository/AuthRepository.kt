package com.mohali.pharmacy.data.repository

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.mohali.pharmacy.data.model.AppUser
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.tasks.await
import javax.inject.Inject
import javax.inject.Singleton

private val Context.ds: DataStore<Preferences> by preferencesDataStore("auth")

@Singleton
class AuthRepository @Inject constructor(
    @ApplicationContext private val ctx: Context,
    private val auth: FirebaseAuth,
    private val db  : FirebaseFirestore
) {
    companion object {
        val K_LOGGED  = booleanPreferencesKey("logged")
        val K_UID     = stringPreferencesKey("uid")
        val K_NAME    = stringPreferencesKey("name")
        val K_ROLE    = stringPreferencesKey("role")
        val K_ADMIN   = booleanPreferencesKey("admin")
    }

    val isLoggedIn  : Flow<Boolean> = ctx.ds.data.map { it[K_LOGGED] ?: false }
    val isAdmin     : Flow<Boolean> = ctx.ds.data.map { it[K_ADMIN]  ?: false }
    val currentRole : Flow<String>  = ctx.ds.data.map { it[K_ROLE]   ?: "" }
    val currentUid  : Flow<String>  = ctx.ds.data.map { it[K_UID]    ?: "" }
    val currentName : Flow<String>  = ctx.ds.data.map { it[K_NAME]   ?: "" }

    suspend fun loginAdmin(user: String, pass: String): Result<Unit> =
        if (user == "admin" && pass == "123456") {
            ctx.ds.edit {
                it[K_LOGGED] = true; it[K_UID] = "admin"
                it[K_NAME] = "المدير"; it[K_ROLE] = "admin"; it[K_ADMIN] = true
            }
            Result.success(Unit)
        } else Result.failure(Exception("اسم المستخدم أو كلمة المرور غير صحيحة"))

    suspend fun loginUser(email: String, pass: String): Result<AppUser> = try {
        val r   = auth.signInWithEmailAndPassword(email, pass).await()
        val uid = r.user?.uid ?: error("فشل تسجيل الدخول")
        val doc = db.collection("users").document(uid).get().await()
        val u   = doc.data?.let { AppUser.fromMap(it.also { m -> m["uid"] = uid }) }
                  ?: error("المستخدم غير موجود")
        if (!u.isActive) error("الحساب معطل")
        ctx.ds.edit {
            it[K_LOGGED] = true; it[K_UID] = uid
            it[K_NAME] = u.name; it[K_ROLE] = u.role; it[K_ADMIN] = false
        }
        Result.success(u)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun logout() {
        auth.signOut()
        ctx.ds.edit { it.clear() }
    }
}
