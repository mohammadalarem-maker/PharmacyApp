package com.mohali.pharmacy.presentation.users

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mohali.pharmacy.data.model.AppUser
import com.mohali.pharmacy.data.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class UsersUiState(
    val users     : List<AppUser> = emptyList(),
    val isLoading : Boolean       = false,
    val error     : String?       = null,
    val message   : String?       = null
)

@HiltViewModel
class UsersViewModel @Inject constructor(private val repo: UserRepository) : ViewModel() {
    private val _ui = MutableStateFlow(UsersUiState())
    val uiState: StateFlow<UsersUiState> = _ui.asStateFlow()

    init { load() }

    fun load() = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        try {
            _ui.update { it.copy(users = repo.getAll(), isLoading = false) }
        } catch (e: Exception) { _ui.update { it.copy(isLoading = false, error = e.message) } }
    }

    fun createUser(name: String, email: String, pass: String,
                   role: String, perms: List<String>) = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        repo.create(name, email, pass, role, perms).fold(
            onSuccess = { _ui.update { it.copy(isLoading = false, message = "تم إنشاء المستخدم بنجاح") }; load() },
            onFailure = { e -> _ui.update { it.copy(isLoading = false, error = e.message) } }
        )
    }

    fun updateUser(user: AppUser) = viewModelScope.launch {
        try {
            repo.update(user)
            _ui.update { it.copy(message = "تم التحديث") }; load()
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun delete(uid: String) = viewModelScope.launch {
        try {
            repo.delete(uid)
            _ui.update { it.copy(users = _ui.value.users.filter { u -> u.uid != uid },
                message = "تم حذف المستخدم") }
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun setActive(uid: String, active: Boolean) = viewModelScope.launch {
        try {
            repo.setActive(uid, active); load()
        } catch (e: Exception) { _ui.update { it.copy(error = e.message) } }
    }

    fun getById(uid: String) = _ui.value.users.firstOrNull { it.uid == uid }
    fun clearMsg() = _ui.update { it.copy(message = null, error = null) }
}
