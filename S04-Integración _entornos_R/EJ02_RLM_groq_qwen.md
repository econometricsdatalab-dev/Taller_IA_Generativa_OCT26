```r
# ==============================================================================
# Estimación y Validación de Regresión Lineal Múltiple (RLM)
# Datos: mtcars | Y: mpg | X: cyl, disp, wt
# Nivel: Presentación Académica
# ==============================================================================

library(tidyverse)
library(car)       # VIF, Breusch-Pagan, Durbin-Watson
library(lmtest)    # Durbin-Watson, Breusch-Pagan (alternativa)
library(sandwich)  # Se necesita para algunos tests
library(olsrr)     # Resumen coleccionado
library(broom)     # Tidy statistics
library(viridis)   # Paleta de colores profesional
library(ggrepel)   # Etiquetas sin solapamiento en gráficos
library(patchwork) # Composición de gráficos

# ------------------------------------------------------------------------------
# 1. PREPARACIÓN DE DATOS
# ------------------------------------------------------------------------------
df <- mtcars %>%
  mutate(
    row_id = row_number(),
    car_name = rownames(mtcars)
  ) %>%
  select(car_name, mpg, cyl, disp, wt) %>%
  filter(!is.na(mpg) & !is.na(cyl) & !is.na(disp) & !is.na(wt))

# Normalizar variables para facilitar interpretación de multicolinealidad
# (opcional, pero útil para diagnóstico)
df_norm <- df %>%
  select(mpg, cyl, disp, wt) %>%
  as_tibble() %>%
  mutate(
    cyl_std = (cyl - mean(cyl)) / sd(cyl),
    disp_std = (disp - mean(disp)) / sd(disp),
    wt_std = (wt - mean(wt)) / sd(wt)
  )

# ------------------------------------------------------------------------------
# 2. ESTIMACIÓN DEL MODELO
# ------------------------------------------------------------------------------
model_full <- lm(mpg ~ cyl + disp + wt, data = df)

# Resumen del modelo
summary_model <- summary(model_full)

# Diagnóstico básico
residuals_model <- residuals(model_full)
fitted_model <- fitted(model_full)
leverage_model <- hatvalues(model_full)  # Influencia
cook_dist <- cooks.distance(model_full)

# ------------------------------------------------------------------------------
# 3. VALIDACIÓN DE SUPUESTOS
# ------------------------------------------------------------------------------

# --- 3.1 Multicolinealidad (VIF) ---
vif_values <- vif(model_full)
vif_df <- as_tibble(vif_values) %>%
  tibble() %>%
  bind_rows(.) %>%
  rownames_to_column(var = "variable") %>%
  column_to_rownames("variable") %>%
  as_tibble()

# Mejor extraído directamente:
vif_df <- tibble(
  variable = rownames(vif_values),
  VIF = as.numeric(vif_values)
)

# --- 3.2 Homocedasticidad (Breusch-Pagan Test) ---
bp_test <- bptest(model_full)
bp_p_value <- bp_test$p.value
bp_statistic <- bp_test$statistic

# Residuals vs Fitted para gráfico
bp_intercept <- coef(model_full)[1]

# --- 3.3 Correlación Serial (Durbin-Watson) ---
# Nota: Durbin-Watson es más apropiado para datos panel/serie temporal.
# Para datos de sección cruzada (mtcars), es menos relevante pero se incluye
# por solicitud del usuario. Se interpreta con cautela.
dw_test <- dwtest(model_full)
dw_statistic <- dw_test$statistic
dw_p_value <- dw_test$p.value

# --- 3.4 Normalidad de Residuos (Shapiro-Wilk + QQ Plot) ---
shapiro_test <- shapiro.test(residuals_model)
shapiro_statistic <- shapiro_test$statistic
shapiro_p_value <- shapiro_test$p.value

# Test de Anderson-Darling (complementario)
ad_test_result <- suppressWarnings(
  t.test(residuals_model, mu = 0)
)
# Usamos Jarque-Bera que es estándar en RLM
jb_test <- jarque.bera.test(residuals_model)
jb_statistic <- jb_test$JB
jb_p_value <- jb_test$p.value

# ------------------------------------------------------------------------------
# 4. TABLA DE RESULTADOS (Tidy)
# ------------------------------------------------------------------------------
model_tidy <- tidy(model_full, conf.int = TRUE) %>%
  mutate(
    variable = term,
    estimate = estimate,
    std_error = std.error,
    statistic = statistic,
    p_value = p.value,
    ci_low = conf.low,
    ci_high = conf.high
  )

# Intercept separado
intercept_row <- model_tidy %>% filter(term == "(Intercept)")
slope_rows <- model_tidy %>% filter(term != "(Intercept)")

# Modelo final resumido para presentación
model_summary_df <- tibble(
  Model = "RLM: mpg ~ cyl + disp + wt",
  N = nrow(df),
  R_squared = summary_model$r.squared,
  Adj_R_squared = summary_model$adj.r.squared,
  F_statistic = summary_model$f statistic[1],
  F_p_value = summary_model$fstatistic[2],
  Intercept = intercept_row$estimate,
  Intercept_pvalue = intercept_row$p_value
)

# Coeficientes
coeficients_display <- model_tidy %>%
  filter(term != "(Intercept)") %>%
  select(term, estimate, std_error, statistic, p_value, ci_low, ci_high) %>%
  rename(
    Variable = term,
    Coeficiente = estimate,
    Error_Estandar = std_error,
    t = statistic,
    p_value = p_value,
    IC_inferior = ci_low,
    IC_superior = ci_high
  )

# ------------------------------------------------------------------------------
# 5. GRÁFICOS (Nivel Presentación Académica)
# ------------------------------------------------------------------------------

# Paleta de colores consistente
colors <- list(
  primary = "#2C6E9B",      # Azul profesional
  secondary = "#E6550D",    # Naranja/acento
  success = "#009E73",      # Verde
  warning = "#D95F02",      # Naranja claro
  danger = "#CC79A7",       # Rosa
  neutral = "#636363",
  bg = "white",
  high_vif = "#D62728",
  low_vif = "#1F77B4"
)

# --- Gráfico 1: Scatter matrix de variables relevantes ---
fig1_mpg_scatters <- 
  df %>%
  ggplot() +
  geom_point(aes(x = cyl, y = mpg), color = colors$primary, size = 2.5) +
  geom_smooth(method = "lm", se = TRUE, color = colors$secondary, 
              fill = colors$secondary, alpha = 0.15, linewidth = 0.8) +
  labs(
    title = "Regresión Línea: MPG vs Cilindros (cyl)",
    subtitle = "Relación lineal negativa esperada",
    x = "Número de Cilindros (cyl)",
    y = "Millas por Galón (mpg)"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
    plot.subtitle = element_text(size = 10, hjust = 0.5, color = colors$neutral),
    panel.grid.minor = element_blank(),
    axis.text = element_text(color = colors$neutral)
  ) +
  guides(colour = "none", fill = "none")

fig2_disp_scatters <-
  df %>%
  ggplot() +
  geom_point(aes(x = disp, y = mpg), color = colors$primary, size = 2.5) +
  geom_smooth(method = "lm", se = TRUE, color = colors$secondary,
              fill = colors$secondary, alpha = 0.15, linewidth = 0.8) +
  labs(
    title = "Regresión Línea: MPG vs Desplazamiento (disp)",
    subtitle = "Volumen de motor asociado a consumo",
    x = "Desplazamiento del Motor (disp)",
    y = "Millas por Galón (mpg)"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
    plot.subtitle = element_text(size = 10, hjust = 0.5, color = colors$neutral),
    panel.grid.minor = element_blank(),
    axis.text = element_text(color = colors$neutral)
  )
```