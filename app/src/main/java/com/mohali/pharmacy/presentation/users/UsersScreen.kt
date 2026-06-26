package com.mohali.pharmacy.presentation.users

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
import com.mohali.pharmacy.data.model.AppUser
import com.mohali.pharmacy.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UsersScreen(
    onAddUser : () -> Unit,
    onEditUser: (String) -> Unit,
    vm        : UsersViewModel = hiltViewModel()
) {
    val ui    by vm.uiState.collectAsState()
    val snack = remember { SnackbarHostState() }
    var deleteUid by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(ui.message) { ui.message?.let { snack.showSnackbar(it); vm.clearMsg() } }
    LaunchedEffect(ui.error)   { ui.error?.let   { snack.showSnackbar("خطأ: $it"); vm.clearMsg() } }

    Scaffold(
        snackbarHost = { SnackbarHost(snack) },
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("إدارة المستخدمين", fontWeight = FontWeight.Bold) },
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
            FloatingActionButton(onClick = onAddUser,
                containerColor = PrimaryBlue, contentColor = SurfaceColor) {
                Icon(Icons.Filled.PersonAdd, "إضافة مستخدم")
            }
        }
    ) { pad ->
        if (ui.isLoading) {
            Box(Modifier.fillMaxSize().padding(pad), Alignment.Center) { CircularProgressIndicator() }
        } else if (ui.users.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(pad), Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Filled.PeopleAlt, null, Modifier.size(64.dp), tint = TextHint)
                    Spacer(Modifier.height(16.dp))
                    Text("لا يوجد مستخدمون", color = TextSecondary)
                }
            }
        } else {
            LazyColumn(
                Modifier.fillMaxSize().padding(pad),
                contentPadding = PaddingValues(12.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(ui.users, key = { it.uid }) { user ->
                    UserCard(
                        user     = user,
                        onEdit   = { onEditUser(user.uid) },
                        onDelete = { deleteUid = user.uid },
                        onToggleActive = { vm.setActive(user.uid, !user.isActive) }
                    )
                }
            }
        }
    }

    deleteUid?.let { uid ->
        AlertDialog(
            onDismissRequest = { deleteUid = null },
            title  = { Text("تأكيد الحذف") },
            text   = { Text("هل تريد حذف هذا المستخدم؟") },
            confirmButton = {
                Button(onClick = { vm.delete(uid); deleteUid = null },
                    colors = ButtonDefaults.buttonColors(containerColor = ErrorRed)) {
                    Text("حذف")
                }
            },
            dismissButton = { TextButton(onClick = { deleteUid = null }) { Text("إلغاء") } }
        )
    }
}

@Composable
fun UserCard(
    user          : AppUser,
    onEdit        : () -> Unit,
    onDelete      : () -> Unit,
    onToggleActive: () -> Unit
) {
    val roleColor = when(user.role) {
        "admin" -> PrimaryBlue; "pharmacist" -> SecondaryTeal
        "manager" -> WarningOrange; else -> TextSecondary
    }
    Card(
        modifier  = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(2.dp),
        shape     = RoundedCornerShape(12.dp),
        colors    = CardDefaults.cardColors(
            containerColor = if (!user.isActive) SurfaceColor.copy(0.6f) else SurfaceColor)
    ) {
        Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
            // Avatar
            Surface(color = PrimaryContainer, shape = RoundedCornerShape(24.dp)) {
                Icon(Icons.Filled.Person, null,
                    modifier = Modifier.padding(10.dp).size(28.dp), tint = PrimaryBlue)
            }
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(user.name, fontWeight = FontWeight.SemiBold,
                        style = MaterialTheme.typography.bodyMedium)
                    Spacer(Modifier.width(8.dp))
                    Surface(color = roleColor.copy(0.15f), shape = RoundedCornerShape(6.dp)) {
                        Text(AppUser.ROLE_LABELS[user.role] ?: user.role,
                            Modifier.padding(horizontal=6.dp, vertical=2.dp),
                            style = MaterialTheme.typography.labelSmall, color = roleColor,
                            fontWeight = FontWeight.Medium)
                    }
                }
                Text(user.email, style = MaterialTheme.typography.bodySmall, color = TextSecondary)
                if (user.phone.isNotEmpty())
                    Text(user.phone, style = MaterialTheme.typography.labelSmall, color = TextHint)
                if (!user.isActive) {
                    Text("معطل", style = MaterialTheme.typography.labelSmall, color = ErrorRed,
                        fontWeight = FontWeight.Medium)
                }
            }
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                IconButton(onClick = onEdit, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Filled.Edit, null, tint = PrimaryBlue, modifier = Modifier.size(20.dp))
                }
                IconButton(onClick = onToggleActive, modifier = Modifier.size(36.dp)) {
                    Icon(
                        if (user.isActive) Icons.Filled.ToggleOn else Icons.Filled.ToggleOff,
                        null,
                        tint = if (user.isActive) SuccessGreen else TextHint,
                        modifier = Modifier.size(20.dp)
                    )
                }
                IconButton(onClick = onDelete, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Filled.Delete, null, tint = ErrorRed, modifier = Modifier.size(20.dp))
                }
            }
        }
    }
}
