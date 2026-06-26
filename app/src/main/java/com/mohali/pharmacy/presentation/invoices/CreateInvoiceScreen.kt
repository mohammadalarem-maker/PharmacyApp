package com.mohali.pharmacy.presentation.invoices

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
                                    Icon(Icons.Filled.Remove, null, modifier = Modifier.size(16.dp), tint = ErrorRed)
                                }
                                Text("${ci.quantity}", fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 4.dp))
                                IconButton(onClick = {
                                    cartItems = cartItems.toMutableList().also {
                                        it[i] = it[i].copy(quantity = ci.quantity + 1)
                                    }
                                }, Modifier.size(30.dp)) {
                                    Icon(Icons.Filled.Add, null, modifier = Modifier.size(16.dp), tint = SuccessGreen)
                                }
                                IconButton(onClick = {
                                    cartItems = cartItems.toMutableList().also { it.removeAt(i) }
                                }, Modifier.size(30.dp)) {
                                    Icon(Icons.Filled.Close, null, modifier = Modifier.size(16.dp), tint = ErrorRed)
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
