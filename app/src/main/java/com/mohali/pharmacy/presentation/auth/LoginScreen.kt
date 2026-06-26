package com.mohali.pharmacy.presentation.auth

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.*
import androidx.compose.ui.unit.*
import androidx.hilt.navigation.compose.hiltViewModel
import com.mohali.pharmacy.ui.theme.*

@Composable
fun LoginScreen(onLoginSuccess: () -> Unit, vm: AuthViewModel = hiltViewModel()) {
    val ui by vm.uiState.collectAsState()
    var isAdminMode by remember { mutableStateOf(true) }
    var username    by remember { mutableStateOf("") }
    var email       by remember { mutableStateOf("") }
    var password    by remember { mutableStateOf("") }
    var showPass    by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier.fillMaxSize().background(
            Brush.verticalGradient(listOf(PrimaryBlue, SecondaryTeal))
        ),
        contentAlignment = Alignment.Center
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth(0.9f)
                .padding(16.dp),
            shape  = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = SurfaceColor),
            elevation = CardDefaults.cardElevation(12.dp)
        ) {
            Column(
                modifier = Modifier.padding(28.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Logo
                Icon(Icons.Filled.LocalPharmacy, null,
                    modifier = Modifier.size(72.dp), tint = PrimaryBlue)
                Text("الصيدلية",
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold, color = PrimaryBlue)
                Text("نظام إدارة الصيدلية",
                    style = MaterialTheme.typography.bodyMedium, color = TextSecondary)

                // Mode tabs
                Row(modifier = Modifier.fillMaxWidth()) {
                    FilterChip(
                        selected = isAdminMode,
                        onClick  = { isAdminMode = true },
                        label    = { Text("مدير النظام") },
                        modifier = Modifier.weight(1f).padding(end = 4.dp)
                    )
                    FilterChip(
                        selected = !isAdminMode,
                        onClick  = { isAdminMode = false },
                        label    = { Text("مستخدم") },
                        modifier = Modifier.weight(1f).padding(start = 4.dp)
                    )
                }

                HorizontalDivider()

                if (isAdminMode) {
                    OutlinedTextField(
                        value = username,
                        onValueChange = { username = it },
                        label   = { Text("اسم المستخدم") },
                        leadingIcon = { Icon(Icons.Filled.Person, null) },
                        singleLine  = true,
                        modifier    = Modifier.fillMaxWidth()
                    )
                } else {
                    OutlinedTextField(
                        value = email,
                        onValueChange = { email = it },
                        label   = { Text("البريد الإلكتروني") },
                        leadingIcon = { Icon(Icons.Filled.Email, null) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                        singleLine  = true,
                        modifier    = Modifier.fillMaxWidth()
                    )
                }

                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    label  = { Text("كلمة المرور") },
                    leadingIcon  = { Icon(Icons.Filled.Lock, null) },
                    trailingIcon = {
                        IconButton(onClick = { showPass = !showPass }) {
                            Icon(if (showPass) Icons.Filled.VisibilityOff
                                 else Icons.Filled.Visibility, null)
                        }
                    },
                    visualTransformation = if (showPass) VisualTransformation.None
                                           else PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    singleLine  = true,
                    modifier    = Modifier.fillMaxWidth()
                )

                ui.error?.let {
                    Card(colors = CardDefaults.cardColors(containerColor = ErrorContainer)) {
                        Text(it, modifier = Modifier.padding(12.dp),
                            color = ErrorRed,
                            style = MaterialTheme.typography.bodySmall)
                    }
                }

                Button(
                    onClick = {
                        if (isAdminMode) vm.loginAdmin(username, password, onLoginSuccess)
                        else             vm.loginUser(email, password, onLoginSuccess)
                    },
                    enabled  = !ui.isLoading,
                    modifier = Modifier.fillMaxWidth().height(52.dp),
                    shape    = RoundedCornerShape(12.dp)
                ) {
                    if (ui.isLoading)
                        CircularProgressIndicator(Modifier.size(24.dp), color = SurfaceColor, strokeWidth = 2.dp)
                    else
                        Text("تسجيل الدخول", style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    }
}
