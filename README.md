# 💊 الصيدلية - Pharmacy Management System

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
