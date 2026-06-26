package com.mohali.pharmacy.presentation.dashboard

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
