Aquí tienes un código completo en R diseñado bajo estándares profesionales de análisis 
financiero. 

Este script utiliza `quantmod` para descargar los datos de **Apple Inc. (AAPL)**, `dplyr` para 
transformar el objeto de serie de tiempo en un *data frame* limpio y calcular medias móviles, y 
`ggplot2` junto con `scales` para crear un gráfico estilizado (inspirado en la estética 
minimalista de Apple y Bloomberg).

### Código en R

```R
# ==============================================================================
# SCRIPT DE ANÁLISIS FINANCIERO: APPLE INC. (AAPL)
# Autor: Análisis de Series de Tiempo con ggplot2 y dplyr
# ==============================================================================

# 1. INSTALACIÓN Y CARGA DE PAQUETES
# ------------------------------------------------------------------------------
pckgs <- c("quantmod", "dplyr", "ggplot2", "scales", "zoo")
new_pckgs <- pckgs[!(pckgs %in% installed.packages()[, "Package"])]
if (length(new_pckgs)) install.packages(new_pckgs)

library(quantmod)
library(dplyr)
library(ggplot2)
library(scales)
library(zoo)

# 2. DESCARGA DE DATOS (vía quantmod)
# ------------------------------------------------------------------------------
ticker <- "AAPL"
fecha_inicio <- "2021-01-01"

# Descargar datos de Yahoo Finance
getSymbols(ticker, src = "yahoo", from = fecha_inicio, auto.assign = TRUE)

# 3. TRANSFORMACIÓN DE DATOS (vía dplyr)
# ------------------------------------------------------------------------------
# Convertimos el objeto xts a data.frame y aplicamos transformaciones
df_aapl <- AAPL %>%
  as.data.frame() %>%
  tibble::rownames_to_column(var = "Date") %>%
  mutate(Date = as.Date(Date)) %>%
  rename(
    Open = AAPL.Open,
    High = AAPL.High,
    Low = AAPL.Low,
    Close = AAPL.Close,
    Volume = AAPL.Volume,
    Adjusted = AAPL.Adjusted
  ) %>%
  # Calculamos Medias Móviles (Indicadores Técnicos)
  mutate(
    MA_50  = rollmean(Adjusted, k = 50, fill = NA, align = "right"),
    MA_200 = rollmean(Adjusted, k = 200, fill = NA, align = "right")
  ) %>%
  # Filtramos para visualizar desde 2022 para mayor claridad visual
  filter(Date >= "2022-01-01")

# 4. VISUALIZACIÓN PROFESIONAL (vía ggplot2)
# ------------------------------------------------------------------------------

# Definición de paleta de colores estilo financiero moderno
col_precio <- "#007AFF" # Azul Apple
col_ma50   <- "#FF9500" # Naranja
col_ma200  <- "#FF3B30" # Rojo

ggplot(df_aapl, aes(x = Date)) +
  # Área con degradado bajo la curva de precio
  geom_area(aes(y = Adjusted), fill = col_precio, alpha = 0.08) +
  
  # Líneas de Medias Móviles
  geom_line(aes(y = MA_200, color = "Media Móvil 200 días"), size = 0.6, linetype = "solid", 
na.rm = TRUE) +
  geom_line(aes(y = MA_50, color = "Media Móvil 50 días"), size = 0.6, linetype = "solid", na.rm 
= TRUE) +
  
  # Línea Principal de Precio
  geom_line(aes(y = Adjusted, color = "Precio Cierre Ajustado"), size = 1) +
  
  # Escalas y Formatos
  scale_y_continuous(
    labels = dollar_format(prefix = "$", accuracy = 1),
    position = "right" # Convención en gráficos financieros (eje Y a la derecha)
  ) +
  scale_x_date(
    date_breaks = "3 months",
    date_labels = "%b\n%Y",
    expand = c(0.01, 0.01)
  ) +
  scale_color_manual(
    values = c(
      "Precio Cierre Ajustado" = col_precio,
      "Media Móvil 50 días" = col_ma50,
      "Media Móvil 200 días" = col_ma200
    )
  ) +
  
  # Etiquetas e Información
  labs(
    title = "Apple Inc. (NASDAQ: AAPL) — Rendimiento Bursátil",
    subtitle = "Precio de cierre ajustado e indicadores de tendencia (2022 - Presente)",
    x = NULL,
    y = "Precio por Acción (USD)",
    color = NULL,
    caption = "Fuente: Elaboración propia con datos de Yahoo Finance mediante quantmod."
  ) +
  
  # Tema Visual Limpio y Profesional
  theme_minimal(base_size = 11) +
  theme(
    # Tipografía y Títulos
    plot.title = element_text(face = "bold", size = 15, color = "#1C1C1E", margin = margin(b = 
4)),
    plot.subtitle = element_text(size = 10, color = "#6C6C70", margin = margin(b = 15)),
    plot.caption = element_text(size = 8, color = "#8E8E93", margin = margin(t = 15), hjust = 0),
    
    # Cuadrícula (Grid) limpia
    panel.grid.major.x = element_line(color = "#E5E5EA", size = 0.3, linetype = "dashed"),
    panel.grid.major.y = element_line(color = "#E5E5EA", size = 0.4),
    panel.grid.minor = element_blank(),
    
    # Leyenda arriba a la izquierda
    legend.position = "top",
    legend.justification = "left",
    legend.margin = margin(b = -5, l = -10),
    legend.text = element_text(size = 9, face = "bold", color = "#3A3A3C"),
    legend.key.width = unit(1.2, "cm"),
    
    # Ejes
    axis.text = element_text(size = 9, color = "#3A3A3C"),
    axis.title.y.right = element_text(size = 9, color = "#6C6C70", margin = margin(l = 10)),
    
    # Márgenes de la figura
    plot.margin = margin(t = 20, r = 20, b = 20, l = 20),
    plot.background = element_rect(fill = "#FFFFFF", color = NA)
  )
```

---

### Detalles clave del diseño financiero implementado:

1. **Eje Y a la derecha:** Es el estándar en terminales financieras como Bloomberg o TradingView,
ya que permite leer el precio más reciente de forma inmediata.
2. **Medias Móviles (MA 50 y MA 200):** Se calcularon mediante `rollmean` de la librería `zoo` 
integrada dentro del flujo de `dplyr`. Ayudan a identificar tendencias de corto y largo plazo.
3. **Estética Limpia (Minimalista):**
   * Eliminación del ruido visual mediante la supresión de líneas de cuadrícula secundarias 
(*minor grid*).
   * Uso de sombras ligeras (`geom_area` con baja opacidad) para darle profundidad al gráfico sin
saturarlo.
   * Colores seleccionados cuidadosamente para asegurar contraste accesible y aspecto 
corporativo.
4. **Transformación Tidyverse:** Convertimos el objeto nativo de series de tiempo (`xts`) que 
devuelve `quantmod` a un formato `tibble/data.frame` para manipularlo cómodamente con sintaxis 
`dplyr` (`mutate`, `rename`, `filter`)