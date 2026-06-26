package com.mohali.pharmacy.presentation.dashboard

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
