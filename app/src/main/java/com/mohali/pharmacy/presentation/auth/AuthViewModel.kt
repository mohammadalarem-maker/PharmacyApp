package com.mohali.pharmacy.presentation.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mohali.pharmacy.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class AuthUiState(
    val isLoading: Boolean = false,
    val error    : String? = null
)

@HiltViewModel
class AuthViewModel @Inject constructor(private val repo: AuthRepository) : ViewModel() {

    private val _ui = MutableStateFlow(AuthUiState())
    val uiState: StateFlow<AuthUiState> = _ui.asStateFlow()

    val isAdmin  : Flow<Boolean> = repo.isAdmin
    val isLogged : Flow<Boolean> = repo.isLoggedIn
    val userName : Flow<String>  = repo.currentName

    fun loginAdmin(user: String, pass: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            _ui.update { it.copy(isLoading = true, error = null) }
            repo.loginAdmin(user, pass).fold(
                onSuccess = { _ui.update { it.copy(isLoading = false) }; onSuccess() },
                onFailure = { _ui.update { it.copy(isLoading = false, error = it.toString()) } }
            )
        }
    }

    fun loginUser(email: String, pass: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            _ui.update { it.copy(isLoading = true, error = null) }
            repo.loginUser(email, pass).fold(
                onSuccess = { _ui.update { it.copy(isLoading = false) }; onSuccess() },
                onFailure = { e -> _ui.update { it.copy(isLoading = false, error = e.message) } }
            )
        }
    }

    fun logout(onDone: () -> Unit) {
        viewModelScope.launch { repo.logout(); onDone() }
    }
}
