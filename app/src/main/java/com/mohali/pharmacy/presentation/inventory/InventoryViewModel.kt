package com.mohali.pharmacy.presentation.inventory

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
