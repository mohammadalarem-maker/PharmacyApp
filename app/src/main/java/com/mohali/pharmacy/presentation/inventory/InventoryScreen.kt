package com.mohali.pharmacy.presentation.inventory

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
