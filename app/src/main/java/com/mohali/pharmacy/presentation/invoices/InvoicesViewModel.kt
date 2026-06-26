package com.mohali.pharmacy.presentation.invoices

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
