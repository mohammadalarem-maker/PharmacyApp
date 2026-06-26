package com.mohali.pharmacy.ui.theme

import android.app.Activity
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.*

private val PharmacyColors = lightColorScheme(
    primary          = PrimaryBlue,
    onPrimary        = SurfaceColor,
    primaryContainer = PrimaryContainer,
    secondary        = SecondaryTeal,
    onSecondary      = SurfaceColor,
    secondaryContainer = SecondaryContainer,
    background       = BackgroundColor,
    onBackground     = TextPrimary,
    surface          = SurfaceColor,
    onSurface        = TextPrimary,
    surfaceVariant   = BackgroundColor,
    onSurfaceVariant = TextSecondary,
    error            = ErrorRed,
    onError          = SurfaceColor,
    outline          = DividerColor,
)

@Composable
fun PharmacyTheme(content: @Composable () -> Unit) {
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val w = (view.context as Activity).window
            w.statusBarColor = PrimaryBlue.toArgb()
            androidx.core.view.WindowCompat.getInsetsController(w, view)
                .isAppearanceLightStatusBars = false
        }
    }
    MaterialTheme(
        colorScheme = PharmacyColors,
        typography  = PharmacyTypography,
        content = {
            CompositionLocalProvider(
                LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Rtl
            ) { content() }
        }
    )
}
