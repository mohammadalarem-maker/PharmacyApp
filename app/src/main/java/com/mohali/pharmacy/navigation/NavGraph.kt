package com.mohali.pharmacy.navigation
import androidx.navigation.NavGraph.Companion.findStartDestination

import androidx.compose.animation.*
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.*
import androidx.navigation.compose.*
import com.mohali.pharmacy.presentation.auth.AuthViewModel
import com.mohali.pharmacy.presentation.auth.LoginScreen
import com.mohali.pharmacy.presentation.dashboard.DashboardScreen
import com.mohali.pharmacy.presentation.inventory.AddEditProductScreen
import com.mohali.pharmacy.presentation.inventory.InventoryScreen
import com.mohali.pharmacy.presentation.invoices.CreateInvoiceScreen
import com.mohali.pharmacy.presentation.invoices.InvoiceDetailScreen
import com.mohali.pharmacy.presentation.invoices.InvoicesScreen
import com.mohali.pharmacy.presentation.users.AddEditUserScreen
import com.mohali.pharmacy.presentation.users.UsersScreen

data class NavItem(val route: String, val label: String, val icon: ImageVector)

@Composable
fun AppNavigation() {
    val nav = rememberNavController()
    NavHost(nav, startDestination = Screen.Login.route) {
        composable(Screen.Login.route) {
            LoginScreen(onLoginSuccess = {
                nav.navigate(Screen.Main.route) {
                    popUpTo(Screen.Login.route) { inclusive = true }
                }
            })
        }
        composable(Screen.Main.route)  { MainHost(nav) }
        composable(
            route = Screen.AddProduct.route,
            arguments = listOf(navArgument("barcode") { defaultValue = ""; type = NavType.StringType })
        ) { bs ->
            AddEditProductScreen(
                barcode    = bs.arguments?.getString("barcode") ?: "",
                onBack     = { nav.popBackStack() }
            )
        }
        composable(
            route = Screen.EditProduct.route,
            arguments = listOf(navArgument("productId") { type = NavType.StringType })
        ) { bs ->
            AddEditProductScreen(
                productId  = bs.arguments?.getString("productId") ?: "",
                onBack     = { nav.popBackStack() }
            )
        }
        composable(
            route = Screen.InvoiceDetail.route,
            arguments = listOf(navArgument("invoiceId") { type = NavType.StringType })
        ) { bs ->
            InvoiceDetailScreen(
                invoiceId  = bs.arguments?.getString("invoiceId") ?: "",
                onBack     = { nav.popBackStack() }
            )
        }
        composable(Screen.CreateInvoice.route) {
            CreateInvoiceScreen(
                onBack          = { nav.popBackStack() },
                onAddProduct    = { bc -> nav.navigate(Screen.AddProduct.route(bc)) }
            )
        }
        composable(
            route = Screen.AddEditUser.route,
            arguments = listOf(navArgument("uid") { defaultValue = ""; type = NavType.StringType })
        ) { bs ->
            AddEditUserScreen(
                userId = bs.arguments?.getString("uid") ?: "",
                onBack = { nav.popBackStack() }
            )
        }
    }
}

@Composable
fun MainHost(outerNav: NavController, initialBarcode: String = "") {
    val authVm: AuthViewModel = hiltViewModel()
    val isAdmin by authVm.isAdmin.collectAsState(initial = false)
    val innerNav = rememberNavController()

    val items = buildList {
        add(NavItem("dashboard","الرئيسية",   Icons.Filled.Home))
        add(NavItem("inventory","المخزون",    Icons.Filled.Inventory))
        add(NavItem("invoices", "الفواتير",   Icons.Filled.Receipt))
        if (isAdmin) add(NavItem("users","المستخدمين", Icons.Filled.People))
    }

    Scaffold(bottomBar = {
        NavigationBar {
            val cur by innerNav.currentBackStackEntryAsState()
            val route = cur?.destination?.route
            items.forEach { item ->
                NavigationBarItem(
                    selected = route == item.route,
                    onClick  = {
                        innerNav.navigate(item.route) {
                            popUpTo(innerNav.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true; restoreState = true
                        }
                    },
                    icon  = { Icon(item.icon, null) },
                    label = { Text(item.label) }
                )
            }
        }
    }) { pad ->
        NavHost(innerNav, startDestination = "dashboard", modifier = Modifier.padding(pad)) {
            composable("dashboard") {
                DashboardScreen(
                    onAddProduct = { bc -> outerNav.navigate(Screen.AddProduct.route(bc)) },
                    onLogout     = {
                        authVm.logout {
                            outerNav.navigate(Screen.Login.route) {
                                popUpTo(Screen.Main.route) { inclusive = true }
                            }
                        }
                    }
                )
            }
            composable("inventory") {
                InventoryScreen(
                    onAddProduct  = { outerNav.navigate(Screen.AddProduct.route()) },
                    onEditProduct = { id -> outerNav.navigate(Screen.EditProduct.route(id)) }
                )
            }
            composable("invoices") {
                InvoicesScreen(
                    onInvoiceClick  = { id -> outerNav.navigate(Screen.InvoiceDetail.route(id)) },
                    onCreateInvoice = { outerNav.navigate(Screen.CreateInvoice.route) }
                )
            }
            composable("users") {
                UsersScreen(
                    onAddUser  = { outerNav.navigate(Screen.AddEditUser.route()) },
                    onEditUser = { uid -> outerNav.navigate(Screen.AddEditUser.route(uid)) }
                )
            }
        }
    }
}
