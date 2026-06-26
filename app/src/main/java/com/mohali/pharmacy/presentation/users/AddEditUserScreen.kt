package com.mohali.pharmacy.presentation.users

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.*
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohali.pharmacy.data.model.AppUser
import com.mohali.pharmacy.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddEditUserScreen(
    userId: String = "",
    onBack: () -> Unit,
    vm    : UsersViewModel = hiltViewModel()
) {
    val ui       by vm.uiState.collectAsState()
    val isEdit   = userId.isNotEmpty()
    val existing = remember(userId) { if (isEdit) vm.getById(userId) else null }

    var name      by remember { mutableStateOf(existing?.name  ?: "") }
    var email     by remember { mutableStateOf(existing?.email ?: "") }
    var phone     by remember { mutableStateOf(existing?.phone ?: "") }
    var password  by remember { mutableStateOf("") }
    var showPass  by remember { mutableStateOf(false) }
    var role      by remember { mutableStateOf(existing?.role  ?: "cashier") }
    var perms     by remember { mutableStateOf(existing?.permissions?.toMutableSet() ?: mutableSetOf()) }

    val snack = remember { SnackbarHostState() }
    LaunchedEffect(ui.message) { ui.message?.let { snack.showSnackbar(it); vm.clearMsg(); onBack() } }
    LaunchedEffect(ui.error)   { ui.error?.let   { snack.showSnackbar("خطأ: $it"); vm.clearMsg() } }

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text(if (isEdit) "تعديل المستخدم" else "إضافة مستخدم",
                    fontWeight = FontWeight.Bold) },
                navigationIcon = { IconButton(onClick = onBack) {
                    Icon(Icons.Filled.ArrowBack, null, tint = SurfaceColor) }},
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = PrimaryBlue, titleContentColor = SurfaceColor)
            )
        }
    ) { pad ->
        Column(
            Modifier.fillMaxSize().padding(pad).verticalScroll(rememberScrollState()).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            OutlinedTextField(value = name, onValueChange = { name = it },
                label = { Text("الاسم الكامل *") }, leadingIcon = { Icon(Icons.Filled.Person, null) },
                singleLine = true, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp))

            OutlinedTextField(value = email, onValueChange = { email = it },
                label = { Text("البريد الإلكتروني *") }, leadingIcon = { Icon(Icons.Filled.Email, null) },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                singleLine = true, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp),
                enabled = !isEdit)

            if (!isEdit) {
                OutlinedTextField(
                    value = password, onValueChange = { password = it },
                    label = { Text("كلمة المرور *") }, leadingIcon = { Icon(Icons.Filled.Lock, null) },
                    trailingIcon = { IconButton(onClick = { showPass = !showPass }) {
                        Icon(if (showPass) Icons.Filled.VisibilityOff else Icons.Filled.Visibility, null)
                    }},
                    visualTransformation = if (showPass) VisualTransformation.None else PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    singleLine = true, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp)
                )
            }

            OutlinedTextField(value = phone, onValueChange = { phone = it },
                label = { Text("رقم الهاتف") }, leadingIcon = { Icon(Icons.Filled.Phone, null) },
                singleLine = true, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp))

            // Role selection
            Text("الدور", fontWeight = FontWeight.SemiBold, color = PrimaryBlue,
                style = MaterialTheme.typography.titleSmall)
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                AppUser.ROLE_LABELS.forEach { (r, label) ->
                    if (r != "admin") FilterChip(
                        selected = role == r, onClick = { role = r },
                        label = { Text(label, style = MaterialTheme.typography.labelSmall) },
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            // Permissions
            Text("الصلاحيات", fontWeight = FontWeight.SemiBold, color = PrimaryBlue,
                style = MaterialTheme.typography.titleSmall)
            Card(shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.padding(8.dp)) {
                    AppUser.ALL_PERMISSIONS.forEach { perm ->
                        Row(
                            Modifier.fillMaxWidth().padding(vertical = 2.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Checkbox(
                                checked = perms.contains(perm),
                                onCheckedChange = { checked ->
                                    perms = perms.toMutableSet().also {
                                        if (checked) it.add(perm) else it.remove(perm)
                                    }
                                }
                            )
                            Text(AppUser.PERMISSION_LABELS[perm] ?: perm,
                                style = MaterialTheme.typography.bodySmall)
                        }
                    }
                }
            }

            Spacer(Modifier.height(8.dp))
            Button(
                onClick = {
                    if (name.isBlank() || email.isBlank()) return@Button
                    if (isEdit) {
                        existing?.let { u ->
                            vm.updateUser(u.copy(name = name, phone = phone,
                                role = role, permissions = perms.toList()))
                        }
                    } else {
                        if (password.isBlank()) return@Button
                        vm.createUser(name, email, password, role, perms.toList())
                    }
                },
                enabled = !ui.isLoading && name.isNotBlank() && email.isNotBlank() &&
                          (isEdit || password.isNotBlank()),
                modifier = Modifier.fillMaxWidth().height(52.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                if (ui.isLoading) CircularProgressIndicator(Modifier.size(24.dp),
                    color = SurfaceColor, strokeWidth = 2.dp)
                else {
                    Icon(Icons.Filled.Save, null, Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text(if (isEdit) "حفظ التعديلات" else "إنشاء المستخدم",
                        style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    }
}
