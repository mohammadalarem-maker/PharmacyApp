package com.mohali.pharmacy.di

import android.content.Context
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import com.mohali.pharmacy.data.repository.*
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides @Singleton fun firestore()  = FirebaseFirestore.getInstance()
    @Provides @Singleton fun firebaseAuth() = FirebaseAuth.getInstance()
    @Provides @Singleton fun storage()    = FirebaseStorage.getInstance()

    @Provides @Singleton
    fun authRepo(@ApplicationContext ctx: Context, a: FirebaseAuth, d: FirebaseFirestore) =
        AuthRepository(ctx, a, d)

    @Provides @Singleton
    fun productRepo(d: FirebaseFirestore, s: FirebaseStorage) = ProductRepository(d, s)

    @Provides @Singleton
    fun invoiceRepo(d: FirebaseFirestore) = InvoiceRepository(d)

    @Provides @Singleton
    fun userRepo(a: FirebaseAuth, d: FirebaseFirestore) = UserRepository(a, d)
}
