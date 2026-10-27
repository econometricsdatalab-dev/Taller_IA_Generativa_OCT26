Aquí tienes un código completo, robusto y listo para producción. Incluye buenas prácticas como 
manejo de zonas horarias, cálculo de rendimientos logarítmicos (estándar en finanzas 
cuantitativas), un tema visual personalizado "estilo Bloomberg/Reuters" y un panel secundario de 
volumen.

```r
# --- 1. CONFIGURACIÓN Y LIBRERÍAS ---
# install.packages(c("quantmod", "tidyverse", "tidyquant", "scales", "lubridate", "patchwork")) #
Descomenta si faltan

library(quantmod)   # Para getSymbols
library(tidyverse)  # dplyr, ggplot2, tibble
library(tidyquant)  # Helpers financieros para ggplot (geom_ma, theme_tq)
library(scales)     # Formato de ejes profesional (dólares, porcentajes, fechas)
library(lubridate)  # Manejo de fechas robusto
library(patchwork)  # Para combinar gráficos (Precio + Volumen) de forma elegante

# --- 2. PARÁMETROS DE ENTRADA ---
ticker_symbol <- "AAPL"
start_date    <- "2020-01-01" # Ajusta según necesidad
end_date      <- Sys.Date()

# --- 3. DESCARGA Y LIMPIEZA DE DATOS (Pipeline dplyr) ---
# getSymbols devuelve un xts; lo convertimos a tibble inmediatamente para usar dplyr/ggplot
asset_data <- getSymbols(
  Symbols = ticker_symbol,
  src     = "yahoo",
  from    = start_date,
  to      = end_date,
  auto.assign = FALSE, # Crítico: devuelve objeto en lugar de crear variable en .GlobalEnv
  warnings  = FALSE
) %>% 
  # Conversión a tibble preservando el índice de fechas
  tk_tbl(preserve_index = TRUE, rename_index = "date") %>% 
  # Limpieza de nombres (quita el prefijo "AAPL.") -> Open, High, Low, Close, Volume, Adjusted
  rename_with(~ gsub(paste0("^", ticker_symbol, "\\."), "", .x)) %>% 
  # Asegurar tipos de datos correctos
  mutate(
    date = as_date(date),
    # Rendimientos logarítmicos (Continuously Compounded Returns) - Estándar cuantitativo
    log_return = log(Adjusted / lag(Adjusted)),
    # Medias móviles exponenciales (EMA) para análisis técnico
    ema_20 = EMA(Adjusted, n = 20),
    ema_50 = EMA(Adjusted, n = 50),
    ema_200 = EMA(Adjusted, n = 200)
  ) %>% 
  # Eliminar NAs generados por lags/EMAs iniciales
  drop_na() %>% 
  # Filtrar solo días de mercado (opcional, Yahoo suele dar solo días hábiles)
  filter(wday(date) %in% 2:6) 

# --- 4. DEFINICIÓN DE TEMA PROFESIONAL PERSONALIZADO ---
theme_financial <- function(base_size = 11, base_family = "sans") {
  theme_minimal(base_size = base_size, base_family = base_family) %+replace%
    theme(
      # Fondo y Grid
      plot.background   = element_rect(fill = "#FFFFFF", color = NA),
      panel.background  = element_rect(fill = "#F8F9FA", color = NA),
      panel.grid.major  = element_line(color = "#E1E4E8", linewidth = 0.3),
      panel.grid.minor  = element_line(color = "#E1E4E8", linewidth = 0.15),
      panel.grid.minor.x = element_blank(),
      
      # Títulos y Etiquetas
      plot.title        = element_text(face = "bold", size = rel(1.4), color = "#1A1A2E", hjust =
0, margin = margin(b = 4)),
      plot.subtitle     = element_text(size = rel(0.9), color = "#4A4A6A", hjust = 0, margin = 
margin(b = 15)),
      plot.caption      = element_text(size = rel(0.65), color = "#8B8D9A", hjust = 1, margin = 
margin(t = 10)),
      axis.title        = element_text(face = "bold", size = rel(0.8), color = "#333333"),
      axis.text         = element_text(size = rel(0.75), color = "#555555"),
      axis.ticks        = element_line(color = "#CCCCCC", linewidth = 0.3),
      axis.ticks.length = unit(4, "pt"),
      
      # Leyenda
      legend.position   = "top",
      legend.justification = "left",
      legend.direction  = "horizontal",
      legend.title      = element_blank(),
      legend.text       = element_text(size = rel(0.75), color = "#333333"),
      legend.background = element_rect(fill = "transparent", color = NA),
      legend.key.size   = unit(12, "pt"),
      legend.margin     = margin(b = -5),
      
      # Margenes
      plot.margin       = margin(20, 20, 15, 20)
    )
}

# Paleta de colores semánticos (Verde/Rojo financieros estándar + Azules neutros)
cols <- c(
  "price"   = "#1A1A2E",   # Azul oscuro casi negro para precio
  "ema_20"  = "#007BFF",   # Azul vivo (Corto plazo)
  "ema_50"  = "#FFB700",   # Amarillo/ Oro (Medio plazo)
  "ema_200" = "#DC3545",   # Rojo institucional (Largo plazo)
  "vol_up"  = "#28A745",   # Verde alcista
  "vol_dn"  = "#DC3545",   # Rojo bajista
  "ret_pos" = "#28A745",
  "ret_neg" = "#DC3545"
)

# --- 5. CONSTRUCCIÓN DE GRÁFICOS ---

# 5.1 Gráfico Principal: Precio + EMAs
p_price <- ggplot(asset_data, aes(x = date)) +
  # Área sutil debajo del precio (opcional, da profundidad)
  geom_area(aes(y = Adjusted), fill = cols["price"], alpha = 0.04, linewidth = 0) +
  # Línea de Precio (Adjusted Close)
  geom_line(aes(y = Adjusted, color = "Precio (Ajustado)"), linewidth = 0.7, lineend = "round") +
  # EMAs
  geom_line(aes(y = ema_20,  color = "EMA 20"),  linewidth = 0.6, linetype = "solid", alpha = 
0.9) +
  geom_line(aes(y = ema_50,  color = "EMA 50"),  linewidth = 0.6, linetype = "dashed", alpha = 
0.9) +
  geom_line(aes(y = ema_200, color = "EMA 200"), linewidth = 0.7, linetype = "solid", alpha = 
0.95) +
  
  # Escalas y Formato
  scale_y_continuous(
    labels = label_dollar(prefix = "$", accuracy = 0.01, big.mark = ","),
    expand = expansion(mult = c(0.02, 0.05))
  ) +
  scale_x_date(
    date_breaks = "6 months",
    date_labels = "%b %Y",
    expand = expansion(mult = c(0.01, 0.01))
  ) +
  scale_color_manual(values = c(
    "Precio (Ajustado)" = cols["price"],
    "EMA 20"            = cols["ema_20"],
    "EMA 50"            = cols["ema_50"],
    "EMA 200"           = cols["ema_200"]
  )) +
  
  # Etiquetas
  labs(
    title    = paste0(ticker_symbol, " - Análisis Técnico de Precio"),
    subtitle = paste0("Desde ", format(min(asset_data$date), "%B %Y"), " | Datos: Yahoo Finance |
Ajustado por Dividendos/Splits"),
    y        = "Precio (USD)",
    x        = NULL, # Eje X se muestra solo en gráfico inferior
    caption  = "EMA: Media Móvil Exponencial. Precio Ajustado (Adjusted Close)."
  ) +
  theme_financial() +
  theme(
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank(),
    legend.key.width = unit(25, "pt")
  )

# 5.2 Gráfico Inferior: Volumen (Coloreado por dirección del precio)
p_volume <- ggplot(asset_data, aes(x = date)) +
  # Determinar color del volumen: Verde si Close >= Open, Rojo en caso contrario
  geom_col(
    aes(y = Volume, fill = Close >= Open), 
    width = 0.8, alpha = 0.7, color = NA, linewidth = 0
  ) +
  scale_fill_manual(values = c("TRUE" = cols["vol_up"], "FALSE" = cols["vol_dn"]), guide = 
"none") +
  scale_y_continuous(
    labels = label_number(scale_cut = cut_short_scale(), suffix = "", big.mark = ","), # 1.2M, 
500K
    expand = expansion(mult = c(0, 0.05))
  ) +
  scale_x_date(
    date_breaks = "6 months",
    date_labels = "%b %Y",
    expand = expansion(mult = c(0.01, 0.01))
  ) +
  labs(y = "Volumen", x = NULL) +
  theme_financial() +
  theme(
    panel.grid.major.x = element_blank(),
    plot.margin = margin(t = -10, r = 20, b = 15, l = 20)
  )

# 5.3 (Opcional) Panel de Rendimientos Logarítmicos - Descomenta si lo necesitas
# p_returns <- ggplot(asset_data, aes(x = date, y = log_return, fill = log_return >= 0)) +
#   geom_col(width = 0.6, alpha = 0.6, color = NA) +
#   geom_hline(yintercept = 0, color = "#333333", linewidth = 0.3) +
#   scale_fill_manual(values = c("TRUE" = cols["ret_pos"], "FALSE" = cols["ret_neg"]), guide = 
"none") +
#   scale_y_continuous(labels = label_percent(accuracy = 0.1)) +
#   labs(y = "Rend. Log.", x = NULL) + theme_financial()

# --- 6. COMPOSICIÓN FINAL CON PATCHWORK ---
# heights: 70% Precio, 30% Volumen (ajustable)
final_plot <- p_price / p_volume + plot_layout(heights = c(3, 1), guides = "collect") & 
  theme(legend.position = "top")

# --- 7. EXPORTACIÓN ALTA CALIDAD (OPCIONAL) ---
# ggsave(
#   filename = paste0(ticker_symbol, "_Professional_Chart_", Sys.Date(), ".png"),
#   plot     = final_plot,
#   width    = 14, height = 8.5, units = "in", dpi = 320, bg = "white"
# )

# --- 8. VISUALIZAR ---
print(final_plot)
```

### Detalles de las decisiones de diseño "Profesional":

1.  **`tk_tbl(preserve_index = TRUE)` (tidyquant):** Convierte el objeto `xts` de `getSymbols` a 
`tibble` manteniendo la columna de fechas (`date`) como primera columna, listo para 
`dplyr`/`ggplot`.
2.  **Precio Ajustado (`Adjusted`):** Es el estándar de la industria para análisis de series 
temporales, ya que corrige *splits* y dividendos. Las EMAs se calculan sobre este.
3.  **Tema `theme_financial`:**
    *   Fondo gris muy claro (`#F8F9FA`) reduce la fatiga visual vs blanco puro.
    *   Grid suave (`#E1E4E8`) guía la vista sin competir con datos.
    *   Tipografía `sans` (sistema) asegura renderizado nítido en cualquier OS.
    *   Leyenda horizontal en *top-left* estándar en terminales Bloomberg/Refinitiv.
4.  **Colores Semánticos:**
    *   **Precio:** Azul oscuro neutro (autoridad).
    *   **EMA 20 (Corto):** Azul vivo (señal rápida).
    *   **EMA 50 (Medio):** Dorado/Amarillo (atención, soporte/resistencia clave).
    *   **EMA 200 (Largo):** Rojo institucional (línea de "mercado alcista/bajista" definitiva).
    *   **Volumen:** Verde/Rojo condicional (`Close >= Open`) para ver presión 
compradora/vendedora instantánea.
5.  **`patchwork` (`p_price / p_volume`):** Alinea ejes X perfectamente, comparte leyenda 
(`guides = "collect"`) y controla proporciones (`heights = c(3, 1)`).
6.  **Escalas `scales`:** `label_dollar` y `label_number(scale_cut = cut_short_scale())` 
formatean ejes como "$150.25" y "1.2M" automáticamente.
7.  **Rendimientos Logarítmicos:** Calculados en el `mutate` (`log_return`), listos para análisis
de riesgo (VaR, Volatilidad) o un tercer panel.

### Requisitos previos:
```r
install.packages(c("quantmod", "tidyverse", "tidyquant", "scales", "lubridate", "patchwork"))
```

Este código genera un gráfico listo para incluir en informes institucionales, presentaciones de 
*pitch deck* o dashboards Shiny.