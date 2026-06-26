package com.mohali.pharmacy.presentation.invoices

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
