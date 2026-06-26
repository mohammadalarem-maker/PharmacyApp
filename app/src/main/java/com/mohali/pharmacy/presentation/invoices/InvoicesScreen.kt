package com.mohali.pharmacy.presentation.invoices

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
