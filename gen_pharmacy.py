#!/usr/bin/env python3
"""PharmacyApp - نظام إدارة الصيدلية - Android Project Generator"""
import os, stat

BASE = "/home/claude/PharmacyApp"

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ {path}")

def mkx(path):
    full = os.path.join(BASE, path)
    st = os.stat(full)
    os.chmod(full, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

os.makedirs(BASE, exist_ok=True)
print("🏗️  Generating PharmacyApp ...")

# ─────────────────────────────────────────────
# BUILD FILES
# ─────────────────────────────────────────────
w("settings.gradle.kts", """pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "PharmacyApp"
include(":app")
""")

w("build.gradle.kts", """plugins {
    id("com.android.application")         version "8.3.2"          apply false
    id("org.jetbrains.kotlin.android")    version "1.9.22"         apply false
    id("com.google.dagger.hilt.android")  version "2.51.1"         apply false
    id("com.google.devtools.ksp")         version "1.9.22-1.0.17"  apply false
    id("com.google.gms.google-services")  version "4.4.1"          apply false
}
""")

w("app/build.gradle.kts", """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.dagger.hilt.android")
    id("com.google.devtools.ksp")
    id("com.google.gms.google-services")
}

android {
    namespace  = "com.mohali.pharmacy"
    compileSdk = 35

    defaultConfig {
        applicationId          = "com.mohali.pharmacy"
        minSdk                 = 26
        targetSdk              = 35
        versionCode            = 1
        versionName            = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables.useSupportLibrary = true
    }

    buildTypes {
        debug   { isDebuggable = true }
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions   { jvmTarget = "17" }
    buildFeatures   { compose  = true }
    composeOptions  { kotlinCompilerExtensionVersion = "1.5.8" }
    packaging       { resources.excludes += "/META-INF/{AL2.0,LGPL2.1}" }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.02.02")
    implementation(composeBom)
    androidTestImplementation(composeBom)

    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.compose.animation:animation")
    implementation("androidx.navigation:navigation-compose:2.7.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")

    implementation("com.google.dagger:hilt-android:2.51.1")
    ksp("com.google.dagger:hilt-android-compiler:2.51.1")
    implementation("androidx.hilt:hilt-navigation-compose:1.2.0")

    implementation(platform("com.google.firebase:firebase-bom:32.8.1"))
    implementation("com.google.firebase:firebase-firestore-ktx")
    implementation("com.google.firebase:firebase-auth-ktx")
    implementation("com.google.firebase:firebase-storage-ktx")
    implementation("com.google.firebase:firebase-analytics-ktx")

    implementation("io.coil-kt:coil-compose:2.6.0")
    implementation("com.journeyapps:zxing-android-embedded:4.3.0")
    implementation("androidx.datastore:datastore-preferences:1.0.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.7.3")
    implementation("com.google.code.gson:gson:2.10.1")

    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
""")

w("gradle/wrapper/gradle-wrapper.properties",
"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.9-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

w("gradle.properties",
"""org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=false
kotlin.code.style=official
android.nonTransitiveRClass=true
""")

w("app/proguard-rules.pro", "-keep class com.mohali.pharmacy.** { *; }\n")

# ─────────────────────────────────────────────
# GITHUB ACTIONS
# ─────────────────────────────────────────────
w(".github/workflows/build.yml", """name: Build PharmacyApp APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3
        with:
          gradle-version: '8.9'

      - name: Create google-services.json placeholder
        run: |
          if [ ! -f app/google-services.json ]; then
            cp app/google-services.json.placeholder app/google-services.json 2>/dev/null || echo "WARNING: No google-services.json found"
          fi

      - name: Generate Gradle Wrapper
        run: gradle wrapper --gradle-version 8.9

      - name: Make gradlew executable
        run: chmod +x gradlew

      - name: Build Debug APK
        run: ./gradlew assembleDebug --no-daemon

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: pharmacy-debug-apk
          path: app/build/outputs/apk/debug/app-debug.apk
          retention-days: 7
""")

# ─────────────────────────────────────────────
# ANDROID MANIFEST
# ─────────────────────────────────────────────
w("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32"/>
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="28"/>

    <uses-feature android:name="android.hardware.camera" android:required="false" />

    <application
        android:name=".PharmacyApplication"
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.PharmacyApp">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name="com.journeyapps.barcodescanner.CaptureActivity"
            android:screenOrientation="portrait"
            tools:replace="screenOrientation" />

        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
    </application>
</manifest>
""")

# ─────────────────────────────────────────────
# RESOURCES
# ─────────────────────────────────────────────
w("app/src/main/res/values/strings.xml", """<resources>
    <string name="app_name">الصيدلية</string>
</resources>
""")

w("app/src/main/res/values/themes.xml", """<resources>
    <style name="Theme.PharmacyApp" parent="android:Theme.Material.Light.NoActionBar" />
</resources>
""")

w("app/src/main/res/xml/file_paths.xml", """<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-cache-path name="my_images" path="." />
    <cache-path name="cache_images" path="." />
</paths>
""")

w("app/src/main/res/xml/backup_rules.xml", """<?xml version="1.0" encoding="utf-8"?>
<full-backup-content>
    <exclude domain="sharedpref" path="." />
</full-backup-content>
""")

w("app/src/main/res/xml/data_extraction_rules.xml", """<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup>
        <exclude domain="sharedpref" path="." />
    </cloud-backup>
</data-extraction-rules>
""")

# mipmap ic_launcher (simple vector drawable)
launcher_xml = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
  <path android:fillColor="#1565C0"
      android:pathData="M0,0h108v108h-108z"/>
  <path android:fillColor="#FFFFFF"
      android:pathData="M54,20 C35.2,20 20,35.2 20,54 C20,72.8 35.2,88 54,88 C72.8,88 88,72.8 88,54 C88,35.2 72.8,20 54,20Z M46,68 L46,40 L68,54 Z"/>
</vector>
"""
for d in ["mipmap-mdpi","mipmap-hdpi","mipmap-xhdpi","mipmap-xxhdpi","mipmap-xxxhdpi"]:
    w(f"app/src/main/res/{d}/ic_launcher.xml", launcher_xml)
    w(f"app/src/main/res/{d}/ic_launcher_round.xml", launcher_xml)

# ─────────────────────────────────────────────
# APPLICATION + MAIN ACTIVITY
# ─────────────────────────────────────────────
PKG = "app/src/main/java/com/mohali/pharmacy"

w(f"{PKG}/PharmacyApplication.kt", """package com.mohali.pharmacy

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class PharmacyApplication : Application()
""")

w(f"{PKG}/MainActivity.kt", """package com.mohali.pharmacy

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.mohali.pharmacy.navigation.AppNavigation
import com.mohali.pharmacy.ui.theme.PharmacyTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            PharmacyTheme {
                Surface(modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background) {
                    AppNavigation()
                }
            }
        }
    }
}
""")

# ─────────────────────────────────────────────
# THEME
# ─────────────────────────────────────────────
w(f"{PKG}/ui/theme/Color.kt", """package com.mohali.pharmacy.ui.theme

import androidx.compose.ui.graphics.Color

val PrimaryBlue      = Color(0xFF1565C0)
val PrimaryDark      = Color(0xFF003C8F)
val PrimaryLight     = Color(0xFF5E92F3)
val PrimaryContainer = Color(0xFFE3F2FD)

val SecondaryTeal    = Color(0xFF00897B)
val SecondaryLight   = Color(0xFF4DB6AC)
val SecondaryContainer = Color(0xFFE0F2F1)

val BackgroundColor  = Color(0xFFF3F4F6)
val SurfaceColor     = Color(0xFFFFFFFF)
val DividerColor     = Color(0xFFE2E8F0)

val TextPrimary      = Color(0xFF1A1A2E)
val TextSecondary    = Color(0xFF64748B)
val TextHint         = Color(0xFFADB5BD)

val SuccessGreen     = Color(0xFF2E7D32)
val SuccessContainer = Color(0xFFE8F5E9)
val WarningOrange    = Color(0xFFE65100)
val WarningContainer = Color(0xFFFFF3E0)
val ErrorRed         = Color(0xFFC62828)
val ErrorContainer   = Color(0xFFFFEBEE)
val LowStockBg       = Color(0xFFFFF8E1)
""")

w(f"{PKG}/ui/theme/Type.kt", """package com.mohali.pharmacy.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val PharmacyTypography = Typography(
    headlineLarge  = TextStyle(fontWeight = FontWeight.Bold,   fontSize = 28.sp, lineHeight = 36.sp),
    headlineMedium = TextStyle(fontWeight = FontWeight.Bold,   fontSize = 24.sp, lineHeight = 32.sp),
    headlineSmall  = TextStyle(fontWeight = FontWeight.SemiBold,fontSize = 20.sp, lineHeight = 28.sp),
    titleLarge     = TextStyle(fontWeight = FontWeight.SemiBold,fontSize = 18.sp, lineHeight = 24.sp),
    titleMedium    = TextStyle(fontWeight = FontWeight.SemiBold,fontSize = 16.sp, lineHeight = 22.sp),
    titleSmall     = TextStyle(fontWeight = FontWeight.Medium,  fontSize = 14.sp, lineHeight = 20.sp),
    bodyLarge      = TextStyle(fontWeight = FontWeight.Normal,  fontSize = 16.sp, lineHeight = 24.sp),
    bodyMedium     = TextStyle(fontWeight = FontWeight.Normal,  fontSize = 14.sp, lineHeight = 20.sp),
    bodySmall      = TextStyle(fontWeight = FontWeight.Normal,  fontSize = 12.sp, lineHeight = 16.sp),
    labelLarge     = TextStyle(fontWeight = FontWeight.Medium,  fontSize = 14.sp, lineHeight = 20.sp),
    labelMedium    = TextStyle(fontWeight = FontWeight.Medium,  fontSize = 12.sp, lineHeight = 16.sp),
    labelSmall     = TextStyle(fontWeight = FontWeight.Medium,  fontSize = 11.sp, lineHeight = 16.sp),
)
""")

w(f"{PKG}/ui/theme/Theme.kt", """package com.mohali.pharmacy.ui.theme

import android.app.Activity
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.*

private val PharmacyColors = lightColorScheme(
    primary          = PrimaryBlue,
    onPrimary        = SurfaceColor,
    primaryContainer = PrimaryContainer,
    secondary        = SecondaryTeal,
    onSecondary      = SurfaceColor,
    secondaryContainer = SecondaryContainer,
    background       = BackgroundColor,
    onBackground     = TextPrimary,
    surface          = SurfaceColor,
    onSurface        = TextPrimary,
    surfaceVariant   = BackgroundColor,
    onSurfaceVariant = TextSecondary,
    error            = ErrorRed,
    onError          = SurfaceColor,
    outline          = DividerColor,
)

@Composable
fun PharmacyTheme(content: @Composable () -> Unit) {
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val w = (view.context as Activity).window
            w.statusBarColor = PrimaryBlue.toArgb()
            androidx.core.view.WindowCompat.getInsetsController(w, view)
                .isAppearanceLightStatusBars = false
        }
    }
    MaterialTheme(
        colorScheme = PharmacyColors,
        typography  = PharmacyTypography,
        content = {
            CompositionLocalProvider(
                LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Rtl
            ) { content() }
        }
    )
}
""")

# ─────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────
w(f"{PKG}/data/model/Product.kt", """package com.mohali.pharmacy.data.model

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
""")

w(f"{PKG}/data/model/Invoice.kt", """package com.mohali.pharmacy.data.model

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
""")

w(f"{PKG}/data/model/AppUser.kt", """package com.mohali.pharmacy.data.model

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
""")

# ─────────────────────────────────────────────
# REPOSITORIES
# ─────────────────────────────────────────────
w(f"{PKG}/data/repository/ProductRepository.kt", """package com.mohali.pharmacy.data.repository

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
""")

w(f"{PKG}/data/repository/InvoiceRepository.kt", """package com.mohali.pharmacy.data.repository

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
""")

w(f"{PKG}/data/repository/AuthRepository.kt", """package com.mohali.pharmacy.data.repository

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
""")

w(f"{PKG}/data/repository/UserRepository.kt", """package com.mohali.pharmacy.data.repository

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
""")

# ─────────────────────────────────────────────
# DI MODULE
# ─────────────────────────────────────────────
w(f"{PKG}/di/AppModule.kt", """package com.mohali.pharmacy.di

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
""")

# ─────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────
w(f"{PKG}/navigation/Screen.kt", """package com.mohali.pharmacy.navigation

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
""")

w(f"{PKG}/navigation/NavGraph.kt", """package com.mohali.pharmacy.navigation

import androidx.compose.animation.*
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.*
import androidx.navigation.compose.*
import com.mohali.pharmacy.presentation.auth.AuthViewModel
import com.mohali.pharmacy.presentation.auth.LoginScreen
import com.mohali.pharmacy.presentation.dashboard.DashboardScreen
import com.mohali.pharmacy.presentation.inventory.AddEditProductScreen
import com.mohali.pharmacy.presentation.inventory.InventoryScreen
import com.mohali.pharmacy.presentation.invoices.CreateInvoiceScreen
import com.mohali.pharmacy.presentation.invoices.InvoiceDetailScreen
import com.mohali.pharmacy.presentation.invoices.InvoicesScreen
import com.mohali.pharmacy.presentation.users.AddEditUserScreen
import com.mohali.pharmacy.presentation.users.UsersScreen

data class NavItem(val route: String, val label: String, val icon: ImageVector)

@Composable
fun AppNavigation() {
    val nav = rememberNavController()
    NavHost(nav, startDestination = Screen.Login.route) {
        composable(Screen.Login.route) {
            LoginScreen(onLoginSuccess = {
                nav.navigate(Screen.Main.route) {
                    popUpTo(Screen.Login.route) { inclusive = true }
                }
            })
        }
        composable(Screen.Main.route)  { MainHost(nav) }
        composable(
            route = Screen.AddProduct.route,
            arguments = listOf(navArgument("barcode") { defaultValue = ""; type = NavType.StringType })
        ) { MainHost(nav, nav.currentBackStackEntry?.arguments?.getString("barcode") ?: ""); }
        composable(
            route = Screen.AddProduct.route,
            arguments = listOf(navArgument("barcode") { defaultValue = ""; type = NavType.StringType })
        ) { bs ->
            AddEditProductScreen(
                barcode    = bs.arguments?.getString("barcode") ?: "",
                onBack     = { nav.popBackStack() }
            )
        }
        composable(
            route = Screen.EditProduct.route,
            arguments = listOf(navArgument("productId") { type = NavType.StringType })
        ) { bs ->
            AddEditProductScreen(
                productId  = bs.arguments?.getString("productId") ?: "",
                onBack     = { nav.popBackStack() }
            )
        }
        composable(
            route = Screen.InvoiceDetail.route,
            arguments = listOf(navArgument("invoiceId") { type = NavType.StringType })
        ) { bs ->
            InvoiceDetailScreen(
                invoiceId  = bs.arguments?.getString("invoiceId") ?: "",
                onBack     = { nav.popBackStack() }
            )
        }
        composable(Screen.CreateInvoice.route) {
            CreateInvoiceScreen(
                onBack          = { nav.popBackStack() },
                onAddProduct    = { bc -> nav.navigate(Screen.AddProduct.route(bc)) }
            )
        }
        composable(
            route = Screen.AddEditUser.route,
            arguments = listOf(navArgument("uid") { defaultValue = ""; type = NavType.StringType })
        ) { bs ->
            AddEditUserScreen(
                userId = bs.arguments?.getString("uid") ?: "",
                onBack = { nav.popBackStack() }
            )
        }
    }
}

@Composable
fun MainHost(outerNav: NavController, initialBarcode: String = "") {
    val authVm: AuthViewModel = hiltViewModel()
    val isAdmin by authVm.isAdmin.collectAsState(initial = false)
    val innerNav = rememberNavController()

    val items = buildList {
        add(NavItem("dashboard","الرئيسية",   Icons.Filled.Home))
        add(NavItem("inventory","المخزون",    Icons.Filled.Inventory))
        add(NavItem("invoices", "الفواتير",   Icons.Filled.Receipt))
        if (isAdmin) add(NavItem("users","المستخدمين", Icons.Filled.People))
    }

    Scaffold(bottomBar = {
        NavigationBar {
            val cur by innerNav.currentBackStackEntryAsState()
            val route = cur?.destination?.route
            items.forEach { item ->
                NavigationBarItem(
                    selected = route == item.route,
                    onClick  = {
                        innerNav.navigate(item.route) {
                            popUpTo(innerNav.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true; restoreState = true
                        }
                    },
                    icon  = { Icon(item.icon, null) },
                    label = { Text(item.label) }
                )
            }
        }
    }) { pad ->
        NavHost(innerNav, startDestination = "dashboard", modifier = Modifier.padding(pad)) {
            composable("dashboard") {
                DashboardScreen(
                    onAddProduct = { bc -> outerNav.navigate(Screen.AddProduct.route(bc)) },
                    onLogout     = {
                        authVm.logout {
                            outerNav.navigate(Screen.Login.route) {
                                popUpTo(Screen.Main.route) { inclusive = true }
                            }
                        }
                    }
                )
            }
            composable("inventory") {
                InventoryScreen(
                    onAddProduct  = { outerNav.navigate(Screen.AddProduct.route()) },
                    onEditProduct = { id -> outerNav.navigate(Screen.EditProduct.route(id)) }
                )
            }
            composable("invoices") {
                InvoicesScreen(
                    onInvoiceClick  = { id -> outerNav.navigate(Screen.InvoiceDetail.route(id)) },
                    onCreateInvoice = { outerNav.navigate(Screen.CreateInvoice.route) }
                )
            }
            composable("users") {
                UsersScreen(
                    onAddUser  = { outerNav.navigate(Screen.AddEditUser.route()) },
                    onEditUser = { uid -> outerNav.navigate(Screen.AddEditUser.route(uid)) }
                )
            }
        }
    }
}
""")

# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
w(f"{PKG}/presentation/auth/AuthViewModel.kt", """package com.mohali.pharmacy.presentation.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mohali.pharmacy.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class AuthUiState(
    val isLoading: Boolean = false,
    val error    : String? = null
)

@HiltViewModel
class AuthViewModel @Inject constructor(private val repo: AuthRepository) : ViewModel() {

    private val _ui = MutableStateFlow(AuthUiState())
    val uiState: StateFlow<AuthUiState> = _ui.asStateFlow()

    val isAdmin  : Flow<Boolean> = repo.isAdmin
    val isLogged : Flow<Boolean> = repo.isLoggedIn
    val userName : Flow<String>  = repo.currentName

    fun loginAdmin(user: String, pass: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            _ui.update { it.copy(isLoading = true, error = null) }
            repo.loginAdmin(user, pass).fold(
                onSuccess = { _ui.update { it.copy(isLoading = false) }; onSuccess() },
                onFailure = { _ui.update { it.copy(isLoading = false, error = it.toString()) } }
            )
        }
    }

    fun loginUser(email: String, pass: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            _ui.update { it.copy(isLoading = true, error = null) }
            repo.loginUser(email, pass).fold(
                onSuccess = { _ui.update { it.copy(isLoading = false) }; onSuccess() },
                onFailure = { e -> _ui.update { it.copy(isLoading = false, error = e.message) } }
            )
        }
    }

    fun logout(onDone: () -> Unit) {
        viewModelScope.launch { repo.logout(); onDone() }
    }
}
""")

w(f"{PKG}/presentation/auth/LoginScreen.kt", """package com.mohali.pharmacy.presentation.auth

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.*
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohali.pharmacy.ui.theme.*

@Composable
fun LoginScreen(onLoginSuccess: () -> Unit, vm: AuthViewModel = hiltViewModel()) {
    val ui by vm.uiState.collectAsState()
    var isAdminMode by remember { mutableStateOf(true) }
    var username    by remember { mutableStateOf("") }
    var email       by remember { mutableStateOf("") }
    var password    by remember { mutableStateOf("") }
    var showPass    by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier.fillMaxSize().background(
            Brush.verticalGradient(listOf(PrimaryBlue, SecondaryTeal))
        ),
        contentAlignment = Alignment.Center
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth(0.9f)
                .padding(16.dp),
            shape  = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceColor),
            elevation = CardDefaults.cardElevation(12.dp)
        ) {
            Column(
                modifier = Modifier.padding(28.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Logo
                Icon(Icons.Filled.LocalPharmacy, null,
                    modifier = Modifier.size(72.dp), tint = PrimaryBlue)
                Text("الصيدلية",
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold, color = PrimaryBlue)
                Text("نظام إدارة الصيدلية",
                    style = MaterialTheme.typography.bodyMedium, color = TextSecondary)

                // Mode tabs
                Row(modifier = Modifier.fillMaxWidth()) {
                    FilterChip(
                        selected = isAdminMode,
                        onClick  = { isAdminMode = true },
                        label    = { Text("مدير النظام") },
                        modifier = Modifier.weight(1f).padding(end = 4.dp)
                    )
                    FilterChip(
                        selected = !isAdminMode,
                        onClick  = { isAdminMode = false },
                        label    = { Text("مستخدم") },
                        modifier = Modifier.weight(1f).padding(start = 4.dp)
                    )
                }

                HorizontalDivider()

                if (isAdminMode) {
                    OutlinedTextField(
                        value = username,
                        onValueChange = { username = it },
                        label   = { Text("اسم المستخدم") },
                        leadingIcon = { Icon(Icons.Filled.Person, null) },
                        singleLine  = true,
                        modifier    = Modifier.fillMaxWidth()
                    )
                } else {
                    OutlinedTextField(
                        value = email,
                        onValueChange = { email = it },
                        label   = { Text("البريد الإلكتروني") },
                        leadingIcon = { Icon(Icons.Filled.Email, null) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                        singleLine  = true,
                        modifier    = Modifier.fillMaxWidth()
                    )
                }

                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    label  = { Text("كلمة المرور") },
                    leadingIcon  = { Icon(Icons.Filled.Lock, null) },
                    trailingIcon = {
                        IconButton(onClick = { showPass = !showPass }) {
                            Icon(if (showPass) Icons.Filled.VisibilityOff
                                 else Icons.Filled.Visibility, null)
                        }
                    },
                    visualTransformation = if (showPass) VisualTransformation.None
                                           else PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    singleLine  = true,
                    modifier    = Modifier.fillMaxWidth()
                )

                ui.error?.let {
                    Card(colors = CardDefaults.cardColors(containerColor = ErrorContainer)) {
                        Text(it, modifier = Modifier.padding(12.dp),
                            color = ErrorRed,
                            style = MaterialTheme.typography.bodySmall)
                    }
                }

                Button(
                    onClick = {
                        if (isAdminMode) vm.loginAdmin(username, password, onLoginSuccess)
                        else             vm.loginUser(email, password, onLoginSuccess)
                    },
                    enabled  = !ui.isLoading,
                    modifier = Modifier.fillMaxWidth().height(52.dp),
                    shape    = RoundedCornerShape(12.dp)
                ) {
                    if (ui.isLoading)
                        CircularProgressIndicator(Modifier.size(24.dp), color = SurfaceColor, strokeWidth = 2.dp)
                    else
                        Text("تسجيل الدخول", style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    }
}
""")

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
w(f"{PKG}/presentation/dashboard/DashboardViewModel.kt", """package com.mohali.pharmacy.presentation.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mohali.pharmacy.data.model.*
import com.mohali.pharmacy.data.repository.InvoiceRepository
import com.mohali.pharmacy.data.repository.ProductRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class DashboardUiState(
    val activeProducts: List<Product> = emptyList(),
    val allProducts   : List<Product> = emptyList(),
    val todaySales    : Double        = 0.0,
    val lowStockCount : Int           = 0,
    val cart          : List<CartItem>= emptyList(),
    val isLoading     : Boolean       = false,
    val error         : String?       = null,
    val message       : String?       = null
)

@HiltViewModel
class DashboardViewModel @Inject constructor(
    private val productRepo: ProductRepository,
    private val invoiceRepo: InvoiceRepository
) : ViewModel() {

    private val _ui = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _ui.asStateFlow()

    init { loadData() }

    fun loadData() = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        try {
            val all    = productRepo.getAll()
            val active = all.filter { it.isActive }
            val low    = all.count { it.quantity <= it.minQuantity && it.isActive }
            val sales  = invoiceRepo.getTodaySales()
            _ui.update { it.copy(allProducts = all, activeProducts = active,
                lowStockCount = low, todaySales = sales, isLoading = false) }
        } catch (e: Exception) {
            _ui.update { it.copy(isLoading = false, error = e.message) }
        }
    }

    fun addToCart(product: Product) {
        val cart = _ui.value.cart.toMutableList()
        val idx  = cart.indexOfFirst { it.product.id == product.id }
        if (idx >= 0) cart[idx] = cart[idx].copy(quantity = cart[idx].quantity + 1)
        else cart.add(CartItem(product))
        _ui.update { it.copy(cart = cart) }
    }

    fun removeFromCart(item: CartItem) {
        _ui.update { it.copy(cart = it.cart.filter { c -> c.product.id != item.product.id }) }
    }

    fun updateCartQty(item: CartItem, qty: Int) {
        if (qty <= 0) { removeFromCart(item); return }
        val cart = _ui.value.cart.map {
            if (it.product.id == item.product.id) it.copy(quantity = qty) else it
        }
        _ui.update { it.copy(cart = cart) }
    }

    fun clearCart() = _ui.update { it.copy(cart = emptyList()) }

    fun confirmPayment(
        customerName  : String,
        customerPhone : String,
        amountPaid    : Double,
        discount      : Double,
        paymentMethod : String,
        createdBy     : String,
        notes         : String
    ) = viewModelScope.launch {
        val cart    = _ui.value.cart
        val items   = cart.map { ci ->
            InvoiceItem(
                productId   = ci.product.id,
                productName = ci.product.name,
                barcode     = ci.product.barcode,
                quantity    = ci.quantity,
                unitPrice   = ci.product.price,
                discount    = ci.discount,
                total       = ci.total
            )
        }
        val subtotal = cart.sumOf { it.total }
        val net      = subtotal - discount
        val change   = amountPaid - net

        val inv = Invoice(
            customerName = customerName, customerPhone = customerPhone,
            items = items, subtotal = subtotal, discount = discount,
            totalAmount = net, amountPaid = amountPaid, change = change,
            paymentMethod = paymentMethod, createdBy = createdBy, notes = notes
        )
        try {
            invoiceRepo.create(inv)
            // Update quantities
            cart.forEach { ci ->
                val newQty = (ci.product.quantity - ci.quantity).coerceAtLeast(0)
                productRepo.updateQty(ci.product.id, newQty)
            }
            _ui.update { it.copy(cart = emptyList(), message = "تم إنجاز عملية البيع بنجاح ✓") }
            loadData()
        } catch (e: Exception) {
            _ui.update { it.copy(error = e.message) }
        }
    }

    fun clearMessage() = _ui.update { it.copy(message = null, error = null) }
}
""")

w(f"{PKG}/presentation/dashboard/DashboardScreen.kt", """package com.mohali.pharmacy.presentation.dashboard

import androidx.compose.animation.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import coil.compose.AsyncImage
import com.mohali.pharmacy.data.model.CartItem
import com.mohali.pharmacy.data.model.Product
import com.mohali.pharmacy.ui.theme.*
import java.text.NumberFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    onAddProduct: (String) -> Unit,
    onLogout    : () -> Unit,
    vm          : DashboardViewModel = hiltViewModel()
) {
    val ui      by vm.uiState.collectAsState()
    var showPay by remember { mutableStateOf(false) }

    // Show snackbar messages
    val snack = remember { SnackbarHostState() }
    LaunchedEffect(ui.message) {
        ui.message?.let { snack.showSnackbar(it); vm.clearMessage() }
    }
    LaunchedEffect(ui.error) {
        ui.error?.let { snack.showSnackbar("خطأ: $it"); vm.clearMessage() }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title  = {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("الصيدلية", fontWeight = FontWeight.Bold)
                        Text("لوحة التحكم",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onPrimary.copy(0.7f))
                    }
                },
                actions = {
                    IconButton(onClick = { vm.loadData() }) {
                        Icon(Icons.Filled.Refresh, "تحديث", tint = SurfaceColor)
                    }
                    IconButton(onClick = onLogout) {
                        Icon(Icons.Filled.Logout, "خروج", tint = SurfaceColor)
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue,
                    titleContentColor = SurfaceColor
                )
            )
        }
    ) { pad ->
        Box(modifier = Modifier.fillMaxSize().padding(pad)) {
            if (ui.isLoading) {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
            } else {
                LazyVerticalGrid(
                    columns = GridCells.Fixed(2),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(
                        start = 12.dp, end = 12.dp, top = 12.dp,
                        bottom = if (ui.cart.isNotEmpty()) 280.dp else 12.dp
                    ),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                    verticalArrangement   = Arrangement.spacedBy(10.dp)
                ) {
                    // Stats row
                    item(span = { GridItemSpan(2) }) { StatsRow(ui) }

                    // Section header
                    item(span = { GridItemSpan(2) }) {
                        Row(verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.padding(vertical = 8.dp)) {
                            Icon(Icons.Filled.Apps, null, tint = PrimaryBlue,
                                modifier = Modifier.size(20.dp))
                            Spacer(Modifier.width(8.dp))
                            Text("المنتجات النشطة",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold)
                            Spacer(Modifier.weight(1f))
                            Text("${ui.activeProducts.size} منتج",
                                style = MaterialTheme.typography.labelMedium,
                                color = TextSecondary)
                        }
                    }

                    items(ui.activeProducts) { product ->
                        DashProductCard(product) { vm.addToCart(product) }
                    }
                }
            }

            // Floating Payment Panel
            AnimatedVisibility(
                visible = ui.cart.isNotEmpty(),
                enter   = slideInVertically { it } + fadeIn(),
                exit    = slideOutVertically { it } + fadeOut(),
                modifier = Modifier.align(Alignment.BottomCenter)
            ) {
                PaymentFloatingPanel(
                    cart          = ui.cart,
                    onRemove      = { vm.removeFromCart(it) },
                    onQtyChange   = { item, qty -> vm.updateCartQty(item, qty) },
                    onClear       = { vm.clearCart() },
                    onPay         = { showPay = true }
                )
            }
        }
    }

    if (showPay) {
        PaymentDialog(
            cart      = ui.cart,
            onDismiss = { showPay = false },
            onConfirm = { name, phone, paid, disc, method, notes ->
                vm.confirmPayment(name, phone, paid, disc, method, "admin", notes)
                showPay = false
            }
        )
    }
}

@Composable
fun StatsRow(ui: DashboardUiState) {
    Row(
        Modifier.fillMaxWidth().padding(vertical = 4.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        StatCard("المنتجات", "${ui.allProducts.size}", Icons.Filled.Inventory,
            PrimaryContainer, PrimaryBlue, Modifier.weight(1f))
        StatCard("مبيعات اليوم", formatPrice(ui.todaySales), Icons.Filled.TrendingUp,
            SuccessContainer, SuccessGreen, Modifier.weight(1f))
        StatCard("مخزون منخفض", "${ui.lowStockCount}", Icons.Filled.Warning,
            if (ui.lowStockCount > 0) WarningContainer else SuccessContainer,
            if (ui.lowStockCount > 0) WarningOrange else SuccessGreen, Modifier.weight(1f))
    }
}

@Composable
fun StatCard(label: String, value: String, icon: androidx.compose.ui.graphics.vector.ImageVector,
             bg: Color, fg: Color, modifier: Modifier) {
    Card(modifier = modifier, colors = CardDefaults.cardColors(containerColor = bg),
         elevation = CardDefaults.cardElevation(2.dp),
         shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(10.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(icon, null, tint = fg, modifier = Modifier.size(22.dp))
            Spacer(Modifier.height(4.dp))
            Text(value, style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold, color = fg)
            Text(label, style = MaterialTheme.typography.labelSmall, color = fg.copy(0.8f))
        }
    }
}

@Composable
fun DashProductCard(product: Product, onClick: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth().clickable(onClick = onClick),
        elevation = CardDefaults.cardElevation(3.dp),
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceColor)
    ) {
        Column {
            Box(
                modifier = Modifier.fillMaxWidth().height(120.dp)
                    .background(PrimaryContainer)
            ) {
                if (product.imageUrl.isNotEmpty()) {
                    AsyncImage(
                        model = product.imageUrl, contentDescription = null,
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )
                } else {
                    Icon(Icons.Filled.MedicalServices, null,
                        modifier = Modifier.align(Alignment.Center).size(48.dp),
                        tint = PrimaryBlue.copy(0.4f))
                }
                // Stock badge
                val stockColor = if (product.quantity <= product.minQuantity) WarningOrange else SuccessGreen
                Surface(
                    modifier = Modifier.align(Alignment.TopEnd).padding(6.dp),
                    color = stockColor, shape = RoundedCornerShape(6.dp)
                ) {
                    Text("${product.quantity}",
                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                        style = MaterialTheme.typography.labelSmall,
                        color = SurfaceColor, fontWeight = FontWeight.Bold)
                }
                // Add to cart icon
                Surface(
                    modifier = Modifier.align(Alignment.BottomEnd).padding(6.dp),
                    color = PrimaryBlue, shape = RoundedCornerShape(8.dp)
                ) {
                    Icon(Icons.Filled.AddShoppingCart, null,
                        modifier = Modifier.padding(4.dp).size(18.dp),
                        tint = SurfaceColor)
                }
            }
            Column(Modifier.padding(8.dp)) {
                Text(product.name, style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 2, overflow = TextOverflow.Ellipsis)
                Spacer(Modifier.height(2.dp))
                Text(formatPrice(product.price) + " ر.ي",
                    style = MaterialTheme.typography.labelMedium,
                    color = PrimaryBlue, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun PaymentFloatingPanel(
    cart       : List<CartItem>,
    onRemove   : (CartItem) -> Unit,
    onQtyChange: (CartItem, Int) -> Unit,
    onClear    : () -> Unit,
    onPay      : () -> Unit
) {
    val total = cart.sumOf { it.total }
    Card(
        modifier  = Modifier.fillMaxWidth().heightIn(min = 200.dp, max = 320.dp),
        shape     = RoundedCornerShape(topStart = 20.dp, topEnd = 20.dp),
        elevation = CardDefaults.cardElevation(16.dp),
        colors    = CardDefaults.cardColors(containerColor = SurfaceColor)
    ) {
        Column {
            // Handle bar
            Box(Modifier.fillMaxWidth().padding(top = 8.dp),
                contentAlignment = Alignment.Center) {
                Surface(Modifier.width(40.dp).height(4.dp),
                    color = DividerColor, shape = RoundedCornerShape(2.dp)) {}
            }
            Row(
                Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Filled.ShoppingCart, null, tint = PrimaryBlue)
                    Spacer(Modifier.width(8.dp))
                    Text("السلة", fontWeight = FontWeight.Bold,
                        style = MaterialTheme.typography.titleMedium)
                    Spacer(Modifier.width(8.dp))
                    Surface(color = PrimaryBlue, shape = RoundedCornerShape(12.dp)) {
                        Text("${cart.size}", Modifier.padding(horizontal=8.dp, vertical=2.dp),
                            color = SurfaceColor,
                            style = MaterialTheme.typography.labelSmall)
                    }
                }
                TextButton(onClick = onClear) {
                    Text("مسح الكل", color = ErrorRed,
                        style = MaterialTheme.typography.labelMedium)
                }
            }
            HorizontalDivider()
            // Items list
            Column(Modifier.weight(1f).verticalScroll(rememberScrollState())) {
                cart.forEach { item ->
                    CartItemRow(item = item,
                        onRemove = { onRemove(item) },
                        onQtyChange = { onQtyChange(item, it) })
                }
            }
            HorizontalDivider()
            // Footer
            Row(
                Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text("الإجمالي", style = MaterialTheme.typography.labelMedium,
                        color = TextSecondary)
                    Text(formatPrice(total) + " ر.ي",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold, color = PrimaryBlue)
                }
                Button(onClick = onPay, shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.height(48.dp)) {
                    Icon(Icons.Filled.Payment, null, modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text("دفع الآن", style = MaterialTheme.typography.titleSmall)
                }
            }
        }
    }
}

@Composable
fun CartItemRow(item: CartItem, onRemove: () -> Unit, onQtyChange: (Int) -> Unit) {
    Row(
        Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Image
        Box(Modifier.size(40.dp).clip(RoundedCornerShape(8.dp))
            .background(PrimaryContainer)) {
            if (item.product.imageUrl.isNotEmpty())
                AsyncImage(model = item.product.imageUrl, contentDescription = null,
                    modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
            else Icon(Icons.Filled.MedicalServices, null,
                modifier = Modifier.align(Alignment.Center).size(24.dp),
                tint = PrimaryBlue.copy(0.5f))
        }
        Spacer(Modifier.width(10.dp))
        Column(Modifier.weight(1f)) {
            Text(item.product.name, style = MaterialTheme.typography.bodySmall,
                maxLines = 1, overflow = TextOverflow.Ellipsis)
            Text(formatPrice(item.product.price) + " ر.ي",
                style = MaterialTheme.typography.labelSmall, color = TextSecondary)
        }
        // Qty controls
        Row(verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = { onQtyChange(item.quantity - 1) }, modifier = Modifier.size(32.dp)) {
                Icon(Icons.Filled.Remove, null, tint = ErrorRed, modifier = Modifier.size(18.dp))
            }
            Text("${item.quantity}", style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 4.dp))
            IconButton(onClick = { onQtyChange(item.quantity + 1) }, modifier = Modifier.size(32.dp)) {
                Icon(Icons.Filled.Add, null, tint = SuccessGreen, modifier = Modifier.size(18.dp))
            }
        }
        Spacer(Modifier.width(4.dp))
        Text(formatPrice(item.total), style = MaterialTheme.typography.labelMedium,
            fontWeight = FontWeight.Bold, color = PrimaryBlue)
        IconButton(onClick = onRemove, modifier = Modifier.size(32.dp)) {
            Icon(Icons.Filled.Close, null, tint = ErrorRed, modifier = Modifier.size(16.dp))
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PaymentDialog(
    cart     : List<CartItem>,
    onDismiss: () -> Unit,
    onConfirm: (String, String, Double, Double, String, String) -> Unit
) {
    var customer  by remember { mutableStateOf("") }
    var phone     by remember { mutableStateOf("") }
    var paid      by remember { mutableStateOf("") }
    var discount  by remember { mutableStateOf("0") }
    var method    by remember { mutableStateOf("cash") }
    var notes     by remember { mutableStateOf("") }

    val subtotal = cart.sumOf { it.total }
    val disc     = discount.toDoubleOrNull() ?: 0.0
    val net      = subtotal - disc
    val change   = (paid.toDoubleOrNull() ?: 0.0) - net

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("تأكيد الدفع", fontWeight = FontWeight.Bold) },
        text = {
            Column(
                modifier = Modifier.verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                // Summary
                Card(colors = CardDefaults.cardColors(containerColor = PrimaryContainer)) {
                    Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        InfoRow("الإجمالي الفرعي", formatPrice(subtotal) + " ر.ي")
                        InfoRow("الخصم",           formatPrice(disc) + " ر.ي")
                        HorizontalDivider()
                        InfoRow("الصافي", formatPrice(net) + " ر.ي", bold = true)
                        if (change >= 0)
                            InfoRow("الباقي", formatPrice(change) + " ر.ي", color = SuccessGreen)
                    }
                }
                OutlinedTextField(value = customer, onValueChange = { customer = it },
                    label = { Text("اسم العميل (اختياري)") },
                    singleLine = true, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = phone, onValueChange = { phone = it },
                    label = { Text("رقم الهاتف (اختياري)") },
                    singleLine = true, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = discount, onValueChange = { discount = it },
                    label = { Text("الخصم") },
                    singleLine = true, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = paid, onValueChange = { paid = it },
                    label = { Text("المبلغ المدفوع") },
                    singleLine = true, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = notes, onValueChange = { notes = it },
                    label = { Text("ملاحظات") },
                    singleLine = true, modifier = Modifier.fillMaxWidth())
                // Payment method
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterChip(selected = method == "cash",  onClick = { method = "cash"  },
                        label = { Text("نقدي") }, modifier = Modifier.weight(1f))
                    FilterChip(selected = method == "card",  onClick = { method = "card"  },
                        label = { Text("بطاقة") }, modifier = Modifier.weight(1f))
                    FilterChip(selected = method == "bank",  onClick = { method = "bank"  },
                        label = { Text("تحويل") }, modifier = Modifier.weight(1f))
                }
            }
        },
        confirmButton = {
            Button(onClick = {
                onConfirm(customer, phone,
                    paid.toDoubleOrNull() ?: net, disc, method, notes)
            }) { Text("تأكيد وإصدار فاتورة") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("إلغاء") } }
    )
}

@Composable
fun InfoRow(label: String, value: String, bold: Boolean = false, color: Color = TextPrimary) {
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label, style = MaterialTheme.typography.bodySmall, color = TextSecondary)
        Text(value, style = MaterialTheme.typography.bodySmall,
            fontWeight = if (bold) FontWeight.Bold else FontWeight.Normal, color = color)
    }
}

fun formatPrice(v: Double): String = "%.2f".format(v)
""")

# ─────────────────────────────────────────────
# INVENTORY
# ─────────────────────────────────────────────
w(f"{PKG}/presentation/inventory/InventoryViewModel.kt", """package com.mohali.pharmacy.presentation.inventory

import android.net.Uri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mohali.pharmacy.data.model.Product
import com.mohali.pharmacy.data.repository.ProductRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class InventoryUiState(
    val products  : List<Product> = emptyList(),
    val filtered  : List<Product> = emptyList(),
    val query     : String        = "",
    val isLoading : Boolean       = false,
    val error     : String?       = null,
    val message   : String?       = null
)

@HiltViewModel
class InventoryViewModel @Inject constructor(private val repo: ProductRepository) : ViewModel() {
    private val _ui = MutableStateFlow(InventoryUiState())
    val uiState: StateFlow<InventoryUiState> = _ui.asStateFlow()

    init { load() }

    fun load() = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        try {
            val all = repo.getAll()
            _ui.update { it.copy(products = all, filtered = all, isLoading = false) }
        } catch (e: Exception) { _ui.update { it.copy(isLoading = false, error = e.message) } }
    }

    fun search(q: String) {
        val all = _ui.value.products
        val f   = if (q.isEmpty()) all
                  else all.filter { it.name.contains(q, true) || it.barcode.contains(q, true) }
        _ui.update { it.copy(query = q, filtered = f) }
    }

    fun delete(id: String) = viewModelScope.launch {
        try {
            repo.delete(id)
            val all = _ui.value.products.filter { it.id != id }
            _ui.update { it.copy(products = all, filtered = all, message = "تم الحذف بنجاح") }
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun saveProduct(product: Product, imageUri: Uri?, onDone: () -> Unit) = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        try {
            val id = if (product.id.isEmpty()) repo.add(product) else { repo.update(product); product.id }
            imageUri?.let {
                val url = repo.uploadImage(it, id)
                repo.update(repo.getAll().first { p -> p.id == id }.copy(imageUrl = url))
            }
            _ui.update { it.copy(isLoading = false, message = "تم الحفظ بنجاح") }
            load(); onDone()
        } catch (e: Exception) { _ui.update { it.copy(isLoading = false, error = e.message) } }
    }

    fun getById(id: String): Product? = _ui.value.products.firstOrNull { it.id == id }
    fun clearMsg() = _ui.update { it.copy(message = null, error = null) }
}
""")

w(f"{PKG}/presentation/inventory/InventoryScreen.kt", """package com.mohali.pharmacy.presentation.inventory

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import coil.compose.AsyncImage
import com.google.zxing.integration.android.IntentIntegrator
import com.mohali.pharmacy.data.model.Product
import com.mohali.pharmacy.ui.theme.*
import androidx.activity.compose.LocalOnBackPressedDispatcherOwner

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun InventoryScreen(
    onAddProduct : () -> Unit,
    onEditProduct: (String) -> Unit,
    vm           : InventoryViewModel = hiltViewModel()
) {
    val ui      by vm.uiState.collectAsState()
    val snack   = remember { SnackbarHostState() }
    var deleteId by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(ui.message) { ui.message?.let { snack.showSnackbar(it); vm.clearMsg() } }
    LaunchedEffect(ui.error)   { ui.error?.let   { snack.showSnackbar("خطأ: $it"); vm.clearMsg() } }

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title  = { Text("إدارة المخزون", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = { vm.load() }) { Icon(Icons.Filled.Refresh, null, tint = SurfaceColor) }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue, titleContentColor = SurfaceColor)
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = onAddProduct,
                containerColor = PrimaryBlue, contentColor = SurfaceColor) {
                Icon(Icons.Filled.Add, "إضافة منتج")
            }
        }
    ) { pad ->
        Column(Modifier.fillMaxSize().padding(pad)) {
            // Search bar
            OutlinedTextField(
                value = ui.query,
                onValueChange = { vm.search(it) },
                placeholder   = { Text("بحث بالاسم أو الباركود...") },
                leadingIcon   = { Icon(Icons.Filled.Search, null) },
                modifier      = Modifier.fillMaxWidth().padding(12.dp),
                singleLine    = true,
                shape         = RoundedCornerShape(12.dp),
                trailingIcon  = {
                    if (ui.query.isNotEmpty())
                        IconButton(onClick = { vm.search("") }) {
                            Icon(Icons.Filled.Close, null)
                        }
                }
            )

            if (ui.isLoading) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (ui.filtered.isEmpty()) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Filled.Inventory, null, Modifier.size(64.dp), tint = TextHint)
                        Spacer(Modifier.height(16.dp))
                        Text("لا توجد منتجات", color = TextSecondary)
                    }
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(12.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(ui.filtered, key = { it.id }) { product ->
                        ProductListItem(
                            product  = product,
                            onEdit   = { onEditProduct(product.id) },
                            onDelete = { deleteId = product.id }
                        )
                    }
                }
            }
        }
    }

    deleteId?.let { id ->
        AlertDialog(
            onDismissRequest = { deleteId = null },
            title   = { Text("تأكيد الحذف") },
            text    = { Text("هل أنت متأكد من حذف هذا المنتج؟") },
            confirmButton = {
                Button(onClick = { vm.delete(id); deleteId = null },
                    colors = ButtonDefaults.buttonColors(containerColor = ErrorRed)) {
                    Text("حذف")
                }
            },
            dismissButton = { TextButton(onClick = { deleteId = null }) { Text("إلغاء") } }
        )
    }
}

@Composable
fun ProductListItem(product: Product, onEdit: () -> Unit, onDelete: () -> Unit) {
    Card(
        modifier  = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(2.dp),
        shape     = RoundedCornerShape(12.dp),
        colors    = CardDefaults.cardColors(
            containerColor = if (!product.isActive) SurfaceColor.copy(0.5f) else SurfaceColor
        )
    ) {
        Row(Modifier.padding(10.dp), verticalAlignment = Alignment.CenterVertically) {
            // Image
            Box(Modifier.size(60.dp).clip(RoundedCornerShape(10.dp)).background(PrimaryContainer)) {
                if (product.imageUrl.isNotEmpty())
                    AsyncImage(model = product.imageUrl, contentDescription = null,
                        modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
                else Icon(Icons.Filled.MedicalServices, null,
                    modifier = Modifier.align(Alignment.Center).size(32.dp),
                    tint = PrimaryBlue.copy(0.4f))
            }
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(product.name, style = MaterialTheme.typography.bodyMedium,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1, overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f))
                    if (!product.isActive)
                        Surface(color = ErrorContainer, shape = RoundedCornerShape(4.dp)) {
                            Text("غير نشط", Modifier.padding(horizontal=4.dp, vertical=2.dp),
                                style = MaterialTheme.typography.labelSmall, color = ErrorRed)
                        }
                }
                Text(product.category, style = MaterialTheme.typography.labelSmall,
                    color = TextSecondary)
                Spacer(Modifier.height(4.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    PriceChip("السعر: ${formatPrice(product.price)}", PrimaryContainer, PrimaryBlue)
                    val stockColor = if (product.quantity <= product.minQuantity) WarningOrange else SuccessGreen
                    val stockBg   = if (product.quantity <= product.minQuantity) WarningContainer else SuccessContainer
                    PriceChip("المخزون: ${product.quantity}", stockBg, stockColor)
                }
                if (product.barcode.isNotEmpty())
                    Text("باركود: ${product.barcode}",
                        style = MaterialTheme.typography.labelSmall, color = TextHint)
            }
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                IconButton(onClick = onEdit, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Filled.Edit, "تعديل", tint = PrimaryBlue, modifier = Modifier.size(20.dp))
                }
                IconButton(onClick = onDelete, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Filled.Delete, "حذف", tint = ErrorRed, modifier = Modifier.size(20.dp))
                }
            }
        }
    }
}

@Composable
fun PriceChip(text: String, bg: Color, fg: Color) {
    Surface(color = bg, shape = RoundedCornerShape(6.dp)) {
        Text(text, Modifier.padding(horizontal=6.dp, vertical=2.dp),
            style = MaterialTheme.typography.labelSmall, color = fg, fontWeight = FontWeight.Medium)
    }
}

private fun formatPrice(v: Double) = "%.2f".format(v)
""")

w(f"{PKG}/presentation/inventory/AddEditProductScreen.kt", """package com.mohali.pharmacy.presentation.inventory

import android.content.Context
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.*
import androidx.core.content.FileProvider
import androidx.hilt.navigation.compose.hiltViewModel
import coil.compose.AsyncImage
import com.mohali.pharmacy.data.model.Product
import com.mohali.pharmacy.ui.theme.*
import java.io.File

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddEditProductScreen(
    barcode  : String = "",
    productId: String = "",
    onBack   : () -> Unit,
    vm       : InventoryViewModel = hiltViewModel()
) {
    val ui  by vm.uiState.collectAsState()
    val ctx = LocalContext.current
    val existing = remember(productId) { if (productId.isNotEmpty()) vm.getById(productId) else null }

    var name          by remember { mutableStateOf(existing?.name          ?: "") }
    var bc            by remember { mutableStateOf(existing?.barcode       ?: barcode) }
    var category      by remember { mutableStateOf(existing?.category      ?: "") }
    var price         by remember { mutableStateOf(existing?.price?.toString()         ?: "") }
    var purchasePrice by remember { mutableStateOf(existing?.purchasePrice?.toString() ?: "") }
    var quantity      by remember { mutableStateOf(existing?.quantity?.toString()      ?: "") }
    var minQuantity   by remember { mutableStateOf(existing?.minQuantity?.toString()   ?: "5") }
    var description   by remember { mutableStateOf(existing?.description   ?: "") }
    var expiryDate    by remember { mutableStateOf(existing?.expiryDate    ?: "") }
    var manufacturer  by remember { mutableStateOf(existing?.manufacturer  ?: "") }
    var unit          by remember { mutableStateOf(existing?.unit          ?: "قطعة") }
    var isActive      by remember { mutableStateOf(existing?.isActive      ?: true) }
    var imageUri      by remember { mutableStateOf<Uri?>(null) }
    var existingImage by remember { mutableStateOf(existing?.imageUrl ?: "") }

    val snack = remember { SnackbarHostState() }
    LaunchedEffect(ui.message) { ui.message?.let { snack.showSnackbar(it); vm.clearMsg() } }
    LaunchedEffect(ui.error)   { ui.error?.let   { snack.showSnackbar("خطأ: $it"); vm.clearMsg() } }

    // Camera photo URI
    val photoFile = remember { File(ctx.cacheDir, "photo_${System.currentTimeMillis()}.jpg") }
    val photoUri  = remember {
        FileProvider.getUriForFile(ctx, "${ctx.packageName}.fileprovider", photoFile)
    }

    val galleryLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri -> uri?.let { imageUri = it } }

    val cameraLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.TakePicture()
    ) { ok -> if (ok) imageUri = photoUri }

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title = {
                    Text(if (productId.isEmpty()) "إضافة منتج جديد" else "تعديل المنتج",
                        fontWeight = FontWeight.Bold)
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Filled.ArrowBack, null, tint = SurfaceColor)
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue, titleContentColor = SurfaceColor)
            )
        }
    ) { pad ->
        Column(
            modifier = Modifier.fillMaxSize().padding(pad)
                .verticalScroll(rememberScrollState()).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // ── IMAGE PICKER ──────────────────────────────
            Card(shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(containerColor = PrimaryContainer)) {
                Row(
                    Modifier.fillMaxWidth().padding(10.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    // Preview
                    Box(
                        Modifier.size(70.dp).clip(RoundedCornerShape(10.dp))
                            .background(SurfaceColor)
                    ) {
                        val imgSrc = imageUri ?: if (existingImage.isNotEmpty()) existingImage else null
                        if (imgSrc != null) {
                            AsyncImage(model = imgSrc, contentDescription = null,
                                modifier = Modifier.fillMaxSize(),
                                contentScale = ContentScale.Crop)
                        } else {
                            Icon(Icons.Filled.Image, null,
                                modifier = Modifier.align(Alignment.Center).size(32.dp),
                                tint = PrimaryBlue.copy(0.5f))
                        }
                    }
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("صورة المنتج",
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.SemiBold, color = PrimaryBlue)
                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            OutlinedButton(
                                onClick = { cameraLauncher.launch(photoUri) },
                                modifier = Modifier.weight(1f).height(34.dp),
                                contentPadding = PaddingValues(horizontal = 4.dp),
                                shape = RoundedCornerShape(8.dp)
                            ) {
                                Icon(Icons.Filled.CameraAlt, null, Modifier.size(14.dp))
                                Spacer(Modifier.width(4.dp))
                                Text("كاميرا", style = MaterialTheme.typography.labelSmall)
                            }
                            OutlinedButton(
                                onClick = { galleryLauncher.launch("image/*") },
                                modifier = Modifier.weight(1f).height(34.dp),
                                contentPadding = PaddingValues(horizontal = 4.dp),
                                shape = RoundedCornerShape(8.dp)
                            ) {
                                Icon(Icons.Filled.PhotoLibrary, null, Modifier.size(14.dp))
                                Spacer(Modifier.width(4.dp))
                                Text("معرض", style = MaterialTheme.typography.labelSmall)
                            }
                        }
                    }
                    if (imageUri != null || existingImage.isNotEmpty()) {
                        IconButton(onClick = { imageUri = null; existingImage = "" },
                            modifier = Modifier.size(28.dp)) {
                            Icon(Icons.Filled.Close, null, tint = ErrorRed,
                                modifier = Modifier.size(16.dp))
                        }
                    }
                }
            }

            // ── FORM FIELDS ───────────────────────────────
            SectionHeader("معلومات المنتج")

            FormField(value = name, onValueChange = { name = it },
                label = "اسم المنتج *", icon = Icons.Filled.MedicalServices)
            FormField(value = bc, onValueChange = { bc = it },
                label = "الباركود", icon = Icons.Filled.QrCode)
            FormField(value = category, onValueChange = { category = it },
                label = "الفئة / التصنيف", icon = Icons.Filled.Category)
            FormField(value = manufacturer, onValueChange = { manufacturer = it },
                label = "الشركة المصنعة", icon = Icons.Filled.Factory)
            FormField(value = expiryDate, onValueChange = { expiryDate = it },
                label = "تاريخ الانتهاء (مثال: 2026/12/31)", icon = Icons.Filled.DateRange)

            SectionHeader("الأسعار والكميات")

            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                FormField(value = price, onValueChange = { price = it },
                    label = "سعر البيع *", icon = Icons.Filled.AttachMoney,
                    keyboardType = KeyboardType.Decimal,
                    modifier = Modifier.weight(1f))
                FormField(value = purchasePrice, onValueChange = { purchasePrice = it },
                    label = "سعر الشراء", icon = Icons.Filled.ShoppingBag,
                    keyboardType = KeyboardType.Decimal,
                    modifier = Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                FormField(value = quantity, onValueChange = { quantity = it },
                    label = "الكمية *", icon = Icons.Filled.Inventory,
                    keyboardType = KeyboardType.Number,
                    modifier = Modifier.weight(1f))
                FormField(value = minQuantity, onValueChange = { minQuantity = it },
                    label = "الحد الأدنى", icon = Icons.Filled.Warning,
                    keyboardType = KeyboardType.Number,
                    modifier = Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                FormField(value = unit, onValueChange = { unit = it },
                    label = "وحدة القياس", icon = Icons.Filled.Scale,
                    modifier = Modifier.weight(1f))
            }

            FormField(value = description, onValueChange = { description = it },
                label = "الوصف", icon = Icons.Filled.Notes, maxLines = 3)

            // Active toggle
            Card(shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = if (isActive) SuccessContainer else ErrorContainer)) {
                Row(
                    Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(if (isActive) Icons.Filled.CheckCircle else Icons.Filled.Cancel,
                            null, tint = if (isActive) SuccessGreen else ErrorRed)
                        Spacer(Modifier.width(10.dp))
                        Text(if (isActive) "المنتج نشط" else "المنتج غير نشط",
                            fontWeight = FontWeight.Medium)
                    }
                    Switch(checked = isActive, onCheckedChange = { isActive = it })
                }
            }

            Spacer(Modifier.height(8.dp))

            // Save button
            Button(
                onClick = {
                    if (name.isBlank() || price.isBlank() || quantity.isBlank()) return@Button
                    val product = Product(
                        id            = productId,
                        name          = name.trim(),
                        barcode       = bc.trim(),
                        category      = category.trim(),
                        price         = price.toDoubleOrNull() ?: 0.0,
                        purchasePrice = purchasePrice.toDoubleOrNull() ?: 0.0,
                        quantity      = quantity.toIntOrNull() ?: 0,
                        minQuantity   = minQuantity.toIntOrNull() ?: 5,
                        description   = description.trim(),
                        expiryDate    = expiryDate.trim(),
                        manufacturer  = manufacturer.trim(),
                        unit          = unit.trim(),
                        isActive      = isActive,
                        imageUrl      = existingImage
                    )
                    vm.saveProduct(product, imageUri, onBack)
                },
                enabled  = !ui.isLoading && name.isNotBlank() && price.isNotBlank(),
                modifier = Modifier.fillMaxWidth().height(52.dp),
                shape    = RoundedCornerShape(12.dp)
            ) {
                if (ui.isLoading)
                    CircularProgressIndicator(Modifier.size(24.dp), color = SurfaceColor, strokeWidth = 2.dp)
                else {
                    Icon(Icons.Filled.Save, null, Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text("حفظ المنتج", style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    }
}

@Composable
fun FormField(
    value         : String,
    onValueChange : (String) -> Unit,
    label         : String,
    icon          : androidx.compose.ui.graphics.vector.ImageVector,
    keyboardType  : KeyboardType = KeyboardType.Text,
    maxLines      : Int          = 1,
    modifier      : Modifier     = Modifier.fillMaxWidth()
) {
    OutlinedTextField(
        value         = value,
        onValueChange = onValueChange,
        label         = { Text(label) },
        leadingIcon   = { Icon(icon, null, Modifier.size(20.dp)) },
        keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
        maxLines      = maxLines,
        shape         = RoundedCornerShape(10.dp),
        modifier      = modifier
    )
}

@Composable
fun SectionHeader(text: String) {
    Row(verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier.padding(vertical = 4.dp)) {
        Surface(color = PrimaryBlue, modifier = Modifier.width(4.dp).height(20.dp),
            shape = RoundedCornerShape(2.dp)) {}
        Spacer(Modifier.width(8.dp))
        Text(text, style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.Bold, color = PrimaryBlue)
    }
}
""")

# ─────────────────────────────────────────────
# INVOICES
# ─────────────────────────────────────────────
w(f"{PKG}/presentation/invoices/InvoicesViewModel.kt", """package com.mohali.pharmacy.presentation.invoices

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mohali.pharmacy.data.model.*
import com.mohali.pharmacy.data.repository.InvoiceRepository
import com.mohali.pharmacy.data.repository.ProductRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class InvoicesUiState(
    val invoices  : List<Invoice> = emptyList(),
    val filtered  : List<Invoice> = emptyList(),
    val selected  : Invoice?      = null,
    val isLoading : Boolean       = false,
    val error     : String?       = null,
    val message   : String?       = null
)

@HiltViewModel
class InvoicesViewModel @Inject constructor(
    private val invoiceRepo: InvoiceRepository,
    private val productRepo: ProductRepository
) : ViewModel() {
    private val _ui = MutableStateFlow(InvoicesUiState())
    val uiState: StateFlow<InvoicesUiState> = _ui.asStateFlow()

    init { load() }

    fun load() = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        try {
            val all = invoiceRepo.getAll()
            _ui.update { it.copy(invoices = all, filtered = all, isLoading = false) }
        } catch (e: Exception) { _ui.update { it.copy(isLoading = false, error = e.message) } }
    }

    fun search(q: String) {
        val f = if (q.isEmpty()) _ui.value.invoices
                else _ui.value.invoices.filter {
                    it.invoiceNumber.contains(q, true) ||
                    it.customerName.contains(q, true)
                }
        _ui.update { it.copy(filtered = f) }
    }

    fun loadById(id: String) = viewModelScope.launch {
        try {
            val inv = invoiceRepo.getById(id)
            _ui.update { it.copy(selected = inv) }
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun delete(id: String) = viewModelScope.launch {
        try {
            invoiceRepo.delete(id)
            val all = _ui.value.invoices.filter { it.id != id }
            _ui.update { it.copy(invoices = all, filtered = all, selected = null,
                message = "تم حذف الفاتورة") }
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun update(inv: Invoice) = viewModelScope.launch {
        try {
            invoiceRepo.update(inv)
            _ui.update { it.copy(selected = inv, message = "تم تحديث الفاتورة") }
            load()
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun createInvoice(inv: Invoice) = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        try {
            invoiceRepo.create(inv)
            inv.items.forEach { item ->
                val products = productRepo.getAll()
                val p = products.firstOrNull { it.id == item.productId }
                p?.let { productRepo.updateQty(it.id, (it.quantity - item.quantity).coerceAtLeast(0)) }
            }
            _ui.update { it.copy(isLoading = false, message = "تم إنشاء الفاتورة بنجاح") }
            load()
        } catch (e: Exception) { _ui.update { it.copy(isLoading = false, error = e.message) } }
    }

    fun clearMsg() = _ui.update { it.copy(message = null, error = null) }
}
""")

w(f"{PKG}/presentation/invoices/InvoicesScreen.kt", """package com.mohali.pharmacy.presentation.invoices

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohali.pharmacy.data.model.Invoice
import com.mohali.pharmacy.ui.theme.*
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun InvoicesScreen(
    onInvoiceClick : (String) -> Unit,
    onCreateInvoice: () -> Unit,
    vm             : InvoicesViewModel = hiltViewModel()
) {
    val ui    by vm.uiState.collectAsState()
    val snack = remember { SnackbarHostState() }
    var query by remember { mutableStateOf("") }

    LaunchedEffect(ui.message) { ui.message?.let { snack.showSnackbar(it); vm.clearMsg() } }

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title  = { Text("الفواتير", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = { vm.load() }) {
                        Icon(Icons.Filled.Refresh, null, tint = SurfaceColor)
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue, titleContentColor = SurfaceColor)
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = onCreateInvoice,
                containerColor = PrimaryBlue, contentColor = SurfaceColor) {
                Icon(Icons.Filled.Add, "فاتورة جديدة")
            }
        }
    ) { pad ->
        Column(Modifier.fillMaxSize().padding(pad)) {
            OutlinedTextField(
                value = query,
                onValueChange = { query = it; vm.search(it) },
                placeholder   = { Text("بحث برقم الفاتورة أو اسم العميل...") },
                leadingIcon   = { Icon(Icons.Filled.Search, null) },
                modifier      = Modifier.fillMaxWidth().padding(12.dp),
                singleLine    = true, shape = RoundedCornerShape(12.dp),
                trailingIcon  = { if (query.isNotEmpty())
                    IconButton(onClick = { query = ""; vm.search("") }) {
                        Icon(Icons.Filled.Close, null) }
                }
            )

            if (ui.isLoading) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (ui.filtered.isEmpty()) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Filled.Receipt, null, Modifier.size(64.dp), tint = TextHint)
                        Spacer(Modifier.height(16.dp))
                        Text("لا توجد فواتير", color = TextSecondary)
                    }
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(12.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(ui.filtered, key = { it.id }) { inv ->
                        InvoiceListCard(inv) { onInvoiceClick(inv.id) }
                    }
                }
            }
        }
    }
}

@Composable
fun InvoiceListCard(inv: Invoice, onClick: () -> Unit) {
    val fmt = SimpleDateFormat("yyyy/MM/dd HH:mm", Locale.getDefault())
    Card(
        onClick   = onClick,
        modifier  = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(2.dp),
        shape     = RoundedCornerShape(12.dp)
    ) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            // Icon
            Surface(color = PrimaryContainer, shape = RoundedCornerShape(10.dp)) {
                Icon(Icons.Filled.Receipt, null,
                    modifier = Modifier.padding(10.dp).size(24.dp), tint = PrimaryBlue)
            }
            Spacer(Modifier.width(14.dp))
            Column(Modifier.weight(1f)) {
                Text(inv.invoiceNumber.ifEmpty { inv.id.take(8) },
                    fontWeight = FontWeight.Bold,
                    style = MaterialTheme.typography.bodyMedium)
                if (inv.customerName.isNotEmpty())
                    Text(inv.customerName, style = MaterialTheme.typography.bodySmall,
                        color = TextSecondary)
                Text(fmt.format(Date(inv.createdAt)),
                    style = MaterialTheme.typography.labelSmall, color = TextHint)
            }
            Column(horizontalAlignment = Alignment.End) {
                Text("%.2f ر.ي".format(inv.totalAmount),
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold, color = PrimaryBlue)
                Surface(
                    color = if (inv.status == "paid") SuccessContainer else WarningContainer,
                    shape = RoundedCornerShape(6.dp)
                ) {
                    Text(if (inv.status == "paid") "مدفوع" else inv.status,
                        Modifier.padding(horizontal=6.dp, vertical=2.dp),
                        style = MaterialTheme.typography.labelSmall,
                        color = if (inv.status == "paid") SuccessGreen else WarningOrange)
                }
            }
        }
    }
}
""")

w(f"{PKG}/presentation/invoices/InvoiceDetailScreen.kt", """package com.mohali.pharmacy.presentation.invoices

import android.content.Intent
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohali.pharmacy.data.model.Invoice
import com.mohali.pharmacy.data.model.InvoiceItem
import com.mohali.pharmacy.ui.theme.*
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun InvoiceDetailScreen(
    invoiceId: String,
    onBack   : () -> Unit,
    vm       : InvoicesViewModel = hiltViewModel()
) {
    val ui      by vm.uiState.collectAsState()
    val ctx     = LocalContext.current
    val snack   = remember { SnackbarHostState() }
    var editing by remember { mutableStateOf(false) }
    var showDel by remember { mutableStateOf(false) }

    LaunchedEffect(invoiceId)  { vm.loadById(invoiceId) }
    LaunchedEffect(ui.message) { ui.message?.let { snack.showSnackbar(it); vm.clearMsg() } }
    LaunchedEffect(ui.error)   { ui.error?.let   { snack.showSnackbar("خطأ: $it"); vm.clearMsg() } }

    val inv = ui.selected

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text(inv?.invoiceNumber ?: "الفاتورة", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Filled.ArrowBack, null, tint = SurfaceColor)
                    }
                },
                actions = {
                    inv?.let {
                        IconButton(onClick = { editing = !editing }) {
                            Icon(if (editing) Icons.Filled.Close else Icons.Filled.Edit,
                                null, tint = SurfaceColor)
                        }
                        IconButton(onClick = { showDel = true }) {
                            Icon(Icons.Filled.Delete, null, tint = SurfaceColor)
                        }
                        IconButton(onClick = { shareInvoice(ctx, it) }) {
                            Icon(Icons.Filled.Share, null, tint = SurfaceColor)
                        }
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue, titleContentColor = SurfaceColor)
            )
        }
    ) { pad ->
        if (inv == null) {
            Box(Modifier.fillMaxSize().padding(pad), Alignment.Center) {
                CircularProgressIndicator()
            }
        } else if (editing) {
            EditInvoicePanel(inv = inv,
                onSave = { vm.update(it); editing = false },
                onCancel = { editing = false })
        } else {
            InvoiceDetails(inv = inv, modifier = Modifier.padding(pad))
        }
    }

    if (showDel) {
        AlertDialog(
            onDismissRequest = { showDel = false },
            title  = { Text("تأكيد الحذف") },
            text   = { Text("هل تريد حذف هذه الفاتورة نهائياً؟") },
            confirmButton = {
                Button(onClick = { vm.delete(invoiceId); showDel = false; onBack() },
                    colors = ButtonDefaults.buttonColors(containerColor = ErrorRed)) {
                    Text("حذف")
                }
            },
            dismissButton = { TextButton(onClick = { showDel = false }) { Text("إلغاء") } }
        )
    }
}

@Composable
fun InvoiceDetails(inv: Invoice, modifier: Modifier) {
    val fmt = SimpleDateFormat("yyyy/MM/dd HH:mm:ss", Locale.getDefault())
    Column(
        modifier = modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Header card
        Card(colors = CardDefaults.cardColors(containerColor = PrimaryContainer),
            shape = RoundedCornerShape(14.dp)) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                InfoRow2("رقم الفاتورة", inv.invoiceNumber.ifEmpty { inv.id.take(12) })
                InfoRow2("التاريخ",      fmt.format(Date(inv.createdAt)))
                if (inv.customerName.isNotEmpty())
                    InfoRow2("العميل", inv.customerName)
                if (inv.customerPhone.isNotEmpty())
                    InfoRow2("الهاتف", inv.customerPhone)
                InfoRow2("طريقة الدفع",
                    when(inv.paymentMethod) {
                        "cash" -> "نقدي"; "card" -> "بطاقة"; else -> "تحويل بنكي"
                    })
                InfoRow2("الحالة", if (inv.status == "paid") "مدفوع" else inv.status)
                if (inv.createdBy.isNotEmpty()) InfoRow2("أنشأ بواسطة", inv.createdBy)
            }
        }
        // Items
        Text("المنتجات", fontWeight = FontWeight.Bold,
            style = MaterialTheme.typography.titleMedium)
        Card(shape = RoundedCornerShape(12.dp)) {
            Column(Modifier.padding(8.dp)) {
                inv.items.forEachIndexed { i, item ->
                    InvoiceItemRow(item)
                    if (i < inv.items.lastIndex) HorizontalDivider()
                }
            }
        }
        // Totals
        Card(colors = CardDefaults.cardColors(containerColor = PrimaryContainer),
            shape = RoundedCornerShape(12.dp)) {
            Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                InfoRow2("الإجمالي الفرعي", "%.2f ر.ي".format(inv.subtotal))
                if (inv.discount > 0) InfoRow2("الخصم", "%.2f ر.ي".format(inv.discount))
                HorizontalDivider()
                InfoRow2("الصافي", "%.2f ر.ي".format(inv.totalAmount), bold = true)
                if (inv.amountPaid > 0) {
                    InfoRow2("المدفوع", "%.2f ر.ي".format(inv.amountPaid))
                    InfoRow2("الباقي",  "%.2f ر.ي".format(inv.change), color = SuccessGreen)
                }
            }
        }
        if (inv.notes.isNotEmpty()) {
            Card(shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(12.dp)) {
                    Text("ملاحظات", fontWeight = FontWeight.SemiBold,
                        style = MaterialTheme.typography.bodySmall, color = TextSecondary)
                    Spacer(Modifier.height(4.dp))
                    Text(inv.notes, style = MaterialTheme.typography.bodyMedium)
                }
            }
        }
    }
}

@Composable
fun InvoiceItemRow(item: InvoiceItem) {
    Row(Modifier.padding(8.dp), verticalAlignment = Alignment.CenterVertically) {
        Column(Modifier.weight(1f)) {
            Text(item.productName, style = MaterialTheme.typography.bodySmall,
                fontWeight = FontWeight.Medium)
            Text("${item.quantity} × %.2f ر.ي".format(item.unitPrice),
                style = MaterialTheme.typography.labelSmall, color = TextSecondary)
        }
        Text("%.2f ر.ي".format(item.total),
            style = MaterialTheme.typography.bodySmall,
            fontWeight = FontWeight.Bold, color = PrimaryBlue)
    }
}

@Composable
fun InfoRow2(label: String, value: String, bold: Boolean = false, color: androidx.compose.ui.graphics.Color = TextPrimary) {
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label, style = MaterialTheme.typography.bodySmall, color = TextSecondary)
        Text(value, style = MaterialTheme.typography.bodySmall,
            fontWeight = if (bold) FontWeight.Bold else FontWeight.Normal, color = color)
    }
}

@Composable
fun EditInvoicePanel(inv: Invoice, onSave: (Invoice) -> Unit, onCancel: () -> Unit) {
    var customer by remember { mutableStateOf(inv.customerName) }
    var phone    by remember { mutableStateOf(inv.customerPhone) }
    var notes    by remember { mutableStateOf(inv.notes) }
    var status   by remember { mutableStateOf(inv.status) }
    var discount by remember { mutableStateOf(inv.discount.toString()) }

    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("تعديل الفاتورة", fontWeight = FontWeight.Bold,
            style = MaterialTheme.typography.titleLarge, color = PrimaryBlue)
        OutlinedTextField(value = customer, onValueChange = { customer = it },
            label = { Text("اسم العميل") }, singleLine = true, modifier = Modifier.fillMaxWidth())
        OutlinedTextField(value = phone, onValueChange = { phone = it },
            label = { Text("رقم الهاتف") }, singleLine = true, modifier = Modifier.fillMaxWidth())
        OutlinedTextField(value = discount, onValueChange = { discount = it },
            label = { Text("الخصم") }, singleLine = true, modifier = Modifier.fillMaxWidth())
        OutlinedTextField(value = notes, onValueChange = { notes = it },
            label = { Text("ملاحظات") }, modifier = Modifier.fillMaxWidth())
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            FilterChip(selected = status=="paid", onClick = { status="paid" },
                label = { Text("مدفوع") }, modifier = Modifier.weight(1f))
            FilterChip(selected = status=="pending", onClick = { status="pending" },
                label = { Text("معلق") }, modifier = Modifier.weight(1f))
            FilterChip(selected = status=="cancelled", onClick = { status="cancelled" },
                label = { Text("ملغي") }, modifier = Modifier.weight(1f))
        }
        val disc = discount.toDoubleOrNull() ?: inv.discount
        val net  = inv.subtotal - disc
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            OutlinedButton(onClick = onCancel, modifier = Modifier.weight(1f)) { Text("إلغاء") }
            Button(onClick = { onSave(inv.copy(customerName = customer, customerPhone = phone,
                notes = notes, status = status, discount = disc, totalAmount = net)) },
                modifier = Modifier.weight(1f)) { Text("حفظ التعديلات") }
        }
    }
}

fun shareInvoice(ctx: android.content.Context, inv: Invoice) {
    val sb = StringBuilder()
    sb.appendLine("══════════════════════")
    sb.appendLine("       فاتورة مبيعات")
    sb.appendLine("══════════════════════")
    sb.appendLine("رقم الفاتورة: ${inv.invoiceNumber}")
    sb.appendLine("التاريخ: ${java.text.SimpleDateFormat("yyyy/MM/dd HH:mm", java.util.Locale.getDefault()).format(java.util.Date(inv.createdAt))}")
    if (inv.customerName.isNotEmpty()) sb.appendLine("العميل: ${inv.customerName}")
    sb.appendLine("──────────────────────")
    inv.items.forEach { item ->
        sb.appendLine("${item.productName}")
        sb.appendLine("  ${item.quantity} × ${"%.2f".format(item.unitPrice)} = ${"%.2f".format(item.total)} ر.ي")
    }
    sb.appendLine("──────────────────────")
    if (inv.discount > 0) sb.appendLine("الخصم: ${"%.2f".format(inv.discount)} ر.ي")
    sb.appendLine("الإجمالي: ${"%.2f".format(inv.totalAmount)} ر.ي")
    if (inv.amountPaid > 0) {
        sb.appendLine("المدفوع: ${"%.2f".format(inv.amountPaid)} ر.ي")
        sb.appendLine("الباقي: ${"%.2f".format(inv.change)} ر.ي")
    }
    sb.appendLine("══════════════════════")
    sb.appendLine("شكراً لزيارتكم")

    val intent = Intent(Intent.ACTION_SEND).apply {
        type = "text/plain"
        putExtra(Intent.EXTRA_TEXT, sb.toString())
    }
    ctx.startActivity(Intent.createChooser(intent, "مشاركة الفاتورة"))
}
""")

w(f"{PKG}/presentation/invoices/CreateInvoiceScreen.kt", """package com.mohali.pharmacy.presentation.invoices

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohali.pharmacy.data.model.*
import com.mohali.pharmacy.presentation.inventory.InventoryViewModel
import com.mohali.pharmacy.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreateInvoiceScreen(
    onBack        : () -> Unit,
    onAddProduct  : (String) -> Unit,
    invVm         : InvoicesViewModel  = hiltViewModel(),
    prodVm        : InventoryViewModel = hiltViewModel()
) {
    val invUi  by invVm.uiState.collectAsState()
    val prodUi by prodVm.uiState.collectAsState()
    val snack  = remember { SnackbarHostState() }

    var customer  by remember { mutableStateOf("") }
    var phone     by remember { mutableStateOf("") }
    var notes     by remember { mutableStateOf("") }
    var discount  by remember { mutableStateOf("0") }
    var query     by remember { mutableStateOf("") }
    var method    by remember { mutableStateOf("cash") }
    var cartItems by remember { mutableStateOf(listOf<CartItem>()) }
    var barcodeInput by remember { mutableStateOf("") }

    LaunchedEffect(invUi.message) { invUi.message?.let { snack.showSnackbar(it); invVm.clearMsg() } }
    LaunchedEffect(invUi.error)   { invUi.error?.let   { snack.showSnackbar("خطأ: $it"); invVm.clearMsg() } }

    val subtotal = cartItems.sumOf { it.total }
    val disc     = discount.toDoubleOrNull() ?: 0.0
    val net      = subtotal - disc

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("إنشاء فاتورة", fontWeight = FontWeight.Bold) },
                navigationIcon = { IconButton(onClick = onBack) {
                    Icon(Icons.Filled.ArrowBack, null, tint = SurfaceColor) }},
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue, titleContentColor = SurfaceColor)
            )
        },
        bottomBar = {
            Surface(shadowElevation = 8.dp) {
                Row(Modifier.fillMaxWidth().padding(12.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    OutlinedButton(onClick = onBack, modifier = Modifier.weight(1f)) { Text("إلغاء") }
                    Button(
                        onClick = {
                            if (cartItems.isEmpty()) return@Button
                            val items = cartItems.map { ci ->
                                InvoiceItem(ci.product.id, ci.product.name, ci.product.barcode,
                                    ci.quantity, ci.product.price, ci.discount, ci.total)
                            }
                            val inv = Invoice(
                                customerName = customer, customerPhone = phone,
                                items = items, subtotal = subtotal, discount = disc,
                                totalAmount = net, amountPaid = net,
                                paymentMethod = method, notes = notes, status = "paid"
                            )
                            invVm.createInvoice(inv); onBack()
                        },
                        enabled = cartItems.isNotEmpty() && !invUi.isLoading,
                        modifier = Modifier.weight(2f)
                    ) { Text("إصدار الفاتورة") }
                }
            }
        }
    ) { pad ->
        Column(Modifier.fillMaxSize().padding(pad).verticalScroll(rememberScrollState())
            .padding(12.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {

            // Barcode / Search
            Card(shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = PrimaryContainer)) {
                Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("إضافة منتج", fontWeight = FontWeight.SemiBold, color = PrimaryBlue)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = barcodeInput, onValueChange = { barcodeInput = it },
                            placeholder = { Text("باركود أو اسم المنتج...") },
                            singleLine = true, modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(8.dp),
                            leadingIcon = { Icon(Icons.Filled.Search, null) }
                        )
                        Button(onClick = {
                            val found = prodUi.products.firstOrNull {
                                it.barcode == barcodeInput || it.name.contains(barcodeInput, true)
                            }
                            if (found != null) {
                                val idx = cartItems.indexOfFirst { it.product.id == found.id }
                                cartItems = if (idx >= 0) cartItems.toMutableList().also {
                                    it[idx] = it[idx].copy(quantity = it[idx].quantity + 1)
                                } else cartItems + CartItem(found)
                                barcodeInput = ""
                            } else { onAddProduct(barcodeInput) }
                        }, shape = RoundedCornerShape(8.dp)) { Text("إضافة") }
                    }
                }
            }

            // Cart
            if (cartItems.isNotEmpty()) {
                Text("المنتجات المضافة", fontWeight = FontWeight.Bold,
                    style = MaterialTheme.typography.titleSmall)
                cartItems.forEachIndexed { i, ci ->
                    Card(shape = RoundedCornerShape(10.dp)) {
                        Row(Modifier.padding(10.dp), verticalAlignment = Alignment.CenterVertically) {
                            Column(Modifier.weight(1f)) {
                                Text(ci.product.name, style = MaterialTheme.typography.bodySmall,
                                    fontWeight = FontWeight.Medium)
                                Text("%.2f ر.ي × ${ci.quantity} = %.2f ر.ي".format(ci.product.price, ci.total),
                                    style = MaterialTheme.typography.labelSmall, color = TextSecondary)
                            }
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                IconButton(onClick = {
                                    cartItems = cartItems.toMutableList().also {
                                        if (ci.quantity > 1) it[i] = it[i].copy(quantity = ci.quantity - 1)
                                        else it.removeAt(i)
                                    }
                                }, Modifier.size(30.dp)) {
                                    Icon(Icons.Filled.Remove, null, tint = ErrorRed, Modifier.size(16.dp))
                                }
                                Text("${ci.quantity}", fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 4.dp))
                                IconButton(onClick = {
                                    cartItems = cartItems.toMutableList().also {
                                        it[i] = it[i].copy(quantity = ci.quantity + 1)
                                    }
                                }, Modifier.size(30.dp)) {
                                    Icon(Icons.Filled.Add, null, tint = SuccessGreen, Modifier.size(16.dp))
                                }
                                IconButton(onClick = {
                                    cartItems = cartItems.toMutableList().also { it.removeAt(i) }
                                }, Modifier.size(30.dp)) {
                                    Icon(Icons.Filled.Close, null, tint = ErrorRed, Modifier.size(16.dp))
                                }
                            }
                        }
                    }
                }
            }

            // Customer info
            OutlinedTextField(value = customer, onValueChange = { customer = it },
                label = { Text("اسم العميل (اختياري)") }, singleLine = true,
                modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp))
            OutlinedTextField(value = phone, onValueChange = { phone = it },
                label = { Text("رقم الهاتف") }, singleLine = true,
                modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp))
            OutlinedTextField(value = discount, onValueChange = { discount = it },
                label = { Text("الخصم") }, singleLine = true,
                modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp))
            OutlinedTextField(value = notes, onValueChange = { notes = it },
                label = { Text("ملاحظات") },
                modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp))

            // Payment method
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                FilterChip(selected = method=="cash", onClick={method="cash"},
                    label={Text("نقدي")}, modifier=Modifier.weight(1f))
                FilterChip(selected = method=="card", onClick={method="card"},
                    label={Text("بطاقة")}, modifier=Modifier.weight(1f))
                FilterChip(selected = method=="bank", onClick={method="bank"},
                    label={Text("تحويل")}, modifier=Modifier.weight(1f))
            }

            // Totals
            Card(colors = CardDefaults.cardColors(containerColor = PrimaryContainer),
                shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    InfoRow2("الإجمالي الفرعي", "%.2f ر.ي".format(subtotal))
                    if (disc > 0) InfoRow2("الخصم", "%.2f ر.ي".format(disc))
                    HorizontalDivider()
                    InfoRow2("الصافي", "%.2f ر.ي".format(net), bold = true)
                }
            }
        }
    }
}
""")

# ─────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────
w(f"{PKG}/presentation/users/UsersViewModel.kt", """package com.mohali.pharmacy.presentation.users

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mohali.pharmacy.data.model.AppUser
import com.mohali.pharmacy.data.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class UsersUiState(
    val users     : List<AppUser> = emptyList(),
    val isLoading : Boolean       = false,
    val error     : String?       = null,
    val message   : String?       = null
)

@HiltViewModel
class UsersViewModel @Inject constructor(private val repo: UserRepository) : ViewModel() {
    private val _ui = MutableStateFlow(UsersUiState())
    val uiState: StateFlow<UsersUiState> = _ui.asStateFlow()

    init { load() }

    fun load() = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        try {
            _ui.update { it.copy(users = repo.getAll(), isLoading = false) }
        } catch (e: Exception) { _ui.update { it.copy(isLoading = false, error = e.message) } }
    }

    fun createUser(name: String, email: String, pass: String,
                   role: String, perms: List<String>) = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        repo.create(name, email, pass, role, perms).fold(
            onSuccess = { _ui.update { it.copy(isLoading = false, message = "تم إنشاء المستخدم بنجاح") }; load() },
            onFailure = { e -> _ui.update { it.copy(isLoading = false, error = e.message) } }
        )
    }

    fun updateUser(user: AppUser) = viewModelScope.launch {
        try {
            repo.update(user)
            _ui.update { it.copy(message = "تم التحديث") }; load()
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun delete(uid: String) = viewModelScope.launch {
        try {
            repo.delete(uid)
            _ui.update { it.copy(users = _ui.value.users.filter { u -> u.uid != uid },
                message = "تم حذف المستخدم") }
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun setActive(uid: String, active: Boolean) = viewModelScope.launch {
        try {
            repo.setActive(uid, active); load()
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun getById(uid: String) = _ui.value.users.firstOrNull { it.uid == uid }
    fun clearMsg() = _ui.update { it.copy(message = null, error = null) }
}
""")

w(f"{PKG}/presentation/users/UsersScreen.kt", """package com.mohali.pharmacy.presentation.users

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohali.pharmacy.data.model.AppUser
import com.mohali.pharmacy.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UsersScreen(
    onAddUser : () -> Unit,
    onEditUser: (String) -> Unit,
    vm        : UsersViewModel = hiltViewModel()
) {
    val ui    by vm.uiState.collectAsState()
    val snack = remember { SnackbarHostState() }
    var deleteUid by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(ui.message) { ui.message?.let { snack.showSnackbar(it); vm.clearMsg() } }
    LaunchedEffect(ui.error)   { ui.error?.let   { snack.showSnackbar("خطأ: $it"); vm.clearMsg() } }

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("إدارة المستخدمين", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = { vm.load() }) {
                        Icon(Icons.Filled.Refresh, null, tint = SurfaceColor)
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue, titleContentColor = SurfaceColor)
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = onAddUser,
                containerColor = PrimaryBlue, contentColor = SurfaceColor) {
                Icon(Icons.Filled.PersonAdd, "إضافة مستخدم")
            }
        }
    ) { pad ->
        if (ui.isLoading) {
            Box(Modifier.fillMaxSize().padding(pad), Alignment.Center) { CircularProgressIndicator() }
        } else if (ui.users.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(pad), Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Filled.PeopleAlt, null, Modifier.size(64.dp), tint = TextHint)
                    Spacer(Modifier.height(16.dp))
                    Text("لا يوجد مستخدمون", color = TextSecondary)
                }
            }
        } else {
            LazyColumn(
                Modifier.fillMaxSize().padding(pad),
                contentPadding = PaddingValues(12.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(ui.users, key = { it.uid }) { user ->
                    UserCard(
                        user     = user,
                        onEdit   = { onEditUser(user.uid) },
                        onDelete = { deleteUid = user.uid },
                        onToggleActive = { vm.setActive(user.uid, !user.isActive) }
                    )
                }
            }
        }
    }

    deleteUid?.let { uid ->
        AlertDialog(
            onDismissRequest = { deleteUid = null },
            title  = { Text("تأكيد الحذف") },
            text   = { Text("هل تريد حذف هذا المستخدم؟") },
            confirmButton = {
                Button(onClick = { vm.delete(uid); deleteUid = null },
                    colors = ButtonDefaults.buttonColors(containerColor = ErrorRed)) {
                    Text("حذف")
                }
            },
            dismissButton = { TextButton(onClick = { deleteUid = null }) { Text("إلغاء") } }
        )
    }
}

@Composable
fun UserCard(
    user          : AppUser,
    onEdit        : () -> Unit,
    onDelete      : () -> Unit,
    onToggleActive: () -> Unit
) {
    val roleColor = when(user.role) {
        "admin" -> PrimaryBlue; "pharmacist" -> SecondaryTeal
        "manager" -> WarningOrange; else -> TextSecondary
    }
    Card(
        modifier  = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(2.dp),
        shape     = RoundedCornerShape(12.dp),
        colors    = CardDefaults.cardColors(
            containerColor = if (!user.isActive) SurfaceColor.copy(0.6f) else SurfaceColor)
    ) {
        Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
            // Avatar
            Surface(color = PrimaryContainer, shape = RoundedCornerShape(24.dp)) {
                Icon(Icons.Filled.Person, null,
                    modifier = Modifier.padding(10.dp).size(28.dp), tint = PrimaryBlue)
            }
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(user.name, fontWeight = FontWeight.SemiBold,
                        style = MaterialTheme.typography.bodyMedium)
                    Spacer(Modifier.width(8.dp))
                    Surface(color = roleColor.copy(0.15f), shape = RoundedCornerShape(6.dp)) {
                        Text(AppUser.ROLE_LABELS[user.role] ?: user.role,
                            Modifier.padding(horizontal=6.dp, vertical=2.dp),
                            style = MaterialTheme.typography.labelSmall, color = roleColor,
                            fontWeight = FontWeight.Medium)
                    }
                }
                Text(user.email, style = MaterialTheme.typography.bodySmall, color = TextSecondary)
                if (user.phone.isNotEmpty())
                    Text(user.phone, style = MaterialTheme.typography.labelSmall, color = TextHint)
                if (!user.isActive) {
                    Text("معطل", style = MaterialTheme.typography.labelSmall, color = ErrorRed,
                        fontWeight = FontWeight.Medium)
                }
            }
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                IconButton(onClick = onEdit, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Filled.Edit, null, tint = PrimaryBlue, modifier = Modifier.size(20.dp))
                }
                IconButton(onClick = onToggleActive, modifier = Modifier.size(36.dp)) {
                    Icon(
                        if (user.isActive) Icons.Filled.ToggleOn else Icons.Filled.ToggleOff,
                        null,
                        tint = if (user.isActive) SuccessGreen else TextHint,
                        modifier = Modifier.size(20.dp)
                    )
                }
                IconButton(onClick = onDelete, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Filled.Delete, null, tint = ErrorRed, modifier = Modifier.size(20.dp))
                }
            }
        }
    }
}
""")

w(f"{PKG}/presentation/users/AddEditUserScreen.kt", """package com.mohali.pharmacy.presentation.users

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.*
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohali.pharmacy.data.model.AppUser
import com.mohali.pharmacy.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddEditUserScreen(
    userId: String = "",
    onBack: () -> Unit,
    vm    : UsersViewModel = hiltViewModel()
) {
    val ui       by vm.uiState.collectAsState()
    val isEdit   = userId.isNotEmpty()
    val existing = remember(userId) { if (isEdit) vm.getById(userId) else null }

    var name      by remember { mutableStateOf(existing?.name  ?: "") }
    var email     by remember { mutableStateOf(existing?.email ?: "") }
    var phone     by remember { mutableStateOf(existing?.phone ?: "") }
    var password  by remember { mutableStateOf("") }
    var showPass  by remember { mutableStateOf(false) }
    var role      by remember { mutableStateOf(existing?.role  ?: "cashier") }
    var perms     by remember { mutableStateOf(existing?.permissions?.toMutableSet() ?: mutableSetOf()) }

    val snack = remember { SnackbarHostState() }
    LaunchedEffect(ui.message) { ui.message?.let { snack.showSnackbar(it); vm.clearMsg(); onBack() } }
    LaunchedEffect(ui.error)   { ui.error?.let   { snack.showSnackbar("خطأ: $it"); vm.clearMsg() } }

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text(if (isEdit) "تعديل المستخدم" else "إضافة مستخدم",
                    fontWeight = FontWeight.Bold) },
                navigationIcon = { IconButton(onClick = onBack) {
                    Icon(Icons.Filled.ArrowBack, null, tint = SurfaceColor) }},
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue, titleContentColor = SurfaceColor)
            )
        }
    ) { pad ->
        Column(
            Modifier.fillMaxSize().padding(pad).verticalScroll(rememberScrollState()).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            OutlinedTextField(value = name, onValueChange = { name = it },
                label = { Text("الاسم الكامل *") }, leadingIcon = { Icon(Icons.Filled.Person, null) },
                singleLine = true, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp))

            OutlinedTextField(value = email, onValueChange = { email = it },
                label = { Text("البريد الإلكتروني *") }, leadingIcon = { Icon(Icons.Filled.Email, null) },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                singleLine = true, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp),
                enabled = !isEdit)

            if (!isEdit) {
                OutlinedTextField(
                    value = password, onValueChange = { password = it },
                    label = { Text("كلمة المرور *") }, leadingIcon = { Icon(Icons.Filled.Lock, null) },
                    trailingIcon = { IconButton(onClick = { showPass = !showPass }) {
                        Icon(if (showPass) Icons.Filled.VisibilityOff else Icons.Filled.Visibility, null)
                    }},
                    visualTransformation = if (showPass) VisualTransformation.None else PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    singleLine = true, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp)
                )
            }

            OutlinedTextField(value = phone, onValueChange = { phone = it },
                label = { Text("رقم الهاتف") }, leadingIcon = { Icon(Icons.Filled.Phone, null) },
                singleLine = true, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp))

            // Role selection
            Text("الدور", fontWeight = FontWeight.SemiBold, color = PrimaryBlue,
                style = MaterialTheme.typography.titleSmall)
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                AppUser.ROLE_LABELS.forEach { (r, label) ->
                    if (r != "admin") FilterChip(
                        selected = role == r, onClick = { role = r },
                        label = { Text(label, style = MaterialTheme.typography.labelSmall) },
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            // Permissions
            Text("الصلاحيات", fontWeight = FontWeight.SemiBold, color = PrimaryBlue,
                style = MaterialTheme.typography.titleSmall)
            Card(shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(8.dp)) {
                    AppUser.ALL_PERMISSIONS.forEach { perm ->
                        Row(
                            Modifier.fillMaxWidth().padding(vertical = 2.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Checkbox(
                                checked = perms.contains(perm),
                                onCheckedChange = { checked ->
                                    perms = perms.toMutableSet().also {
                                        if (checked) it.add(perm) else it.remove(perm)
                                    }
                                }
                            )
                            Text(AppUser.PERMISSION_LABELS[perm] ?: perm,
                                style = MaterialTheme.typography.bodySmall)
                        }
                    }
                }
            }

            Spacer(Modifier.height(8.dp))
            Button(
                onClick = {
                    if (name.isBlank() || email.isBlank()) return@Button
                    if (isEdit) {
                        existing?.let { u ->
                            vm.updateUser(u.copy(name = name, phone = phone,
                                role = role, permissions = perms.toList()))
                        }
                    } else {
                        if (password.isBlank()) return@Button
                        vm.createUser(name, email, password, role, perms.toList())
                    }
                },
                enabled = !ui.isLoading && name.isNotBlank() && email.isNotBlank() &&
                          (isEdit || password.isNotBlank()),
                modifier = Modifier.fillMaxWidth().height(52.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                if (ui.isLoading) CircularProgressIndicator(Modifier.size(24.dp),
                    color = SurfaceColor, strokeWidth = 2.dp)
                else {
                    Icon(Icons.Filled.Save, null, Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text(if (isEdit) "حفظ التعديلات" else "إنشاء المستخدم",
                        style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    }
}
""")

# ─────────────────────────────────────────────
# google-services.json placeholder
# ─────────────────────────────────────────────
w("app/google-services.json.placeholder", """{
  "project_info": {
    "project_number": "123456789",
    "project_id": "your-pharmacy-app",
    "storage_bucket": "your-pharmacy-app.appspot.com"
  },
  "client": [
    {
      "client_info": {
        "mobilesdk_app_id": "1:123456789:android:abcdef1234567890",
        "android_client_info": {
          "package_name": "com.mohali.pharmacy"
        }
      },
      "oauth_client": [],
      "api_key": [{"current_key": "YOUR_API_KEY_HERE"}],
      "services": {
        "appinvite_service": {"other_platform_oauth_client": []}
      }
    }
  ],
  "configuration_version": "1"
}
""")

# ─────────────────────────────────────────────
# README
# ─────────────────────────────────────────────
w("README.md", """# 💊 الصيدلية - Pharmacy Management System

نظام إدارة صيدلية متكامل مبني بـ Kotlin + Jetpack Compose + Firebase

## ✨ المميزات
- 🏠 **لوحة تحكم** - عرض المنتجات النشطة + إحصائيات اليوم
- 🛒 **سلة عائمة** - إضافة منتجات مباشرة من الداش بورد
- 📦 **إدارة المخزون** - إضافة/تعديل/حذف المنتجات
- 📸 **رفع الصور** - عبر الكاميرا أو معرض الصور
- 🔍 **بحث بالباركود** - يضيف المنتج للسلة أو يفتح شاشة الإضافة
- 🧾 **الفواتير** - إنشاء/تعديل/حذف/مشاركة الفواتير
- 👥 **المستخدمون** - إضافة/تعديل/حذف + التحكم بالصلاحيات
- 🔐 **مدير محلي** - اسم المستخدم: `admin` | كلمة المرور: `123456`
- ☁️ **Firebase** - مزامنة البيانات فورية

## 🚀 طريقة البناء

### 1. إعداد Firebase
1. أنشئ مشروع في [Firebase Console](https://console.firebase.google.com)
2. أضف تطبيق Android بـ Package: `com.mohali.pharmacy`
3. حمّل `google-services.json` وضعه في مجلد `app/`
4. فعّل: Firestore, Firebase Auth, Storage

### 2. رفع على GitHub ثم البناء
```bash
cd PharmacyApp
git init
git add .
git commit -m "Initial PharmacyApp commit"
git remote add origin https://github.com/USERNAME/PharmacyApp.git
git push -u origin main
```
سيشتغل GitHub Actions تلقائياً وينزل APK من قسم Artifacts.

## 📁 هيكل المشروع
```
app/src/main/java/com/mohali/pharmacy/
├── data/
│   ├── model/     (Product, Invoice, AppUser)
│   └── repository/ (Auth, Product, Invoice, User)
├── di/            (AppModule - Hilt)
├── navigation/    (NavGraph, Screen)
├── presentation/
│   ├── auth/      (Login)
│   ├── dashboard/ (Dashboard + Payment Panel)
│   ├── inventory/ (List + Add/Edit)
│   ├── invoices/  (List + Detail + Create)
│   └── users/     (List + Add/Edit)
└── ui/theme/      (Colors, Theme, Typography)
```
""")

# ─────────────────────────────────────────────
# Fix NavGraph - remove duplicate composable
# ─────────────────────────────────────────────
import re
ng_path = os.path.join(BASE, "app/src/main/java/com/mohali/pharmacy/navigation/NavGraph.kt")
with open(ng_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the duplicate/wrong MainHost call block
fixed = content.replace(
    '''        composable(Screen.Main.route)  { MainHost(nav) }
        composable(
            route = Screen.AddProduct.route,
            arguments = listOf(navArgument("barcode") { defaultValue = ""; type = NavType.StringType })
        ) { MainHost(nav, nav.currentBackStackEntry?.arguments?.getString("barcode") ?: ""); }
        composable(''',
    '''        composable(Screen.Main.route)  { MainHost(nav) }
        composable('''
)
with open(ng_path, 'w', encoding='utf-8') as f:
    f.write(fixed)

print()
print("=" * 50)
print("✅  PharmacyApp generated successfully!")
print(f"📁  Location: {BASE}")
print("=" * 50)
print()
print("📋  Next steps:")
print("  1. Copy PharmacyApp to your Termux/project dir")
print("  2. Add your real google-services.json to app/")
print("  3. git init && git add . && git push to GitHub")
print("  4. GitHub Actions will build the APK")
print()
print("🔐  Admin credentials:")
print("     Username : admin")
print("     Password : 123456")
