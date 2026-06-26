package com.mohali.pharmacy.presentation.inventory

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
