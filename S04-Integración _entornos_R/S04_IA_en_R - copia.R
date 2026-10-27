#/////////////////////////////////////////////////////#
# Taller IA                                           #
# Tema: Integración de IA en R con RStudio            #
# Sesión: 04                                          #
# Fecha: 26/10/2026                                   #
# Instructor: Alexis Adonai Morales Alberto           #
#/////////////////////////////////////////////////////#

# Paquetes para trabajar ----

# tidyverse, ellmer, gander

## Verificar existencia de pacman ----

if(require("pacman", quietly = T)){
  cat("El paquete de pacman se encuentra instalado en esta versión de R")
} else{
  install.packages("pacman", dependencies = T)
}

## Carga de paquetes ----

install.packages("ellmer", dependencies = T)
install.packages("gander", dependencies = T)

# NOTA: Solo se ejecuta una vez, no cada que usemos el script

pacman::p_load(
  "tidyverse",
  "ellmer",
  "gander"
)

# Gemini Google con Ellmer ----

## APIS de google ----

Sys.setenv(GEMINI_API_KEY = "APIKEY")

Sys.setenv(GOOGLE_API_KEY = "APIKEY")


## Revisar qué modelos podemos conectar ----

models_google_gemini(
  base_url = "https://generativelanguage.googleapis.com/v1beta/",
  api_key = "APIKEY",
  credentials = NULL
)

## NOTA: Aquellos con NA en cached_input, input y output no cobra
## pero tiene un limite de tokens por sesión.

## Especificar la conexión al modelo ----

chat <- chat_google_gemini(
  model = "gemini-3.6-flash"
)

## Chat en vivo mediante consola ----

live_console(chat)

# Prompt: Crea código de R, en el que se pueda gráficar una serie de tiempo mediante ggplot2 y usando dplyr. La serie de tiempo las vas conectar con getSymbols para bajar un ticket de un activo financiero, en este caso el activo deberá ser de Apple Inc. El gráfico debe ser muy profesional, limpio y visualmente atractivo para usarse en análisis financiero.

## Enviar prompts al chat directo y la respuesta en consola ----

chat$chat("Crea código de R, en el que se pueda gráficar una serie de tiempo mediante ggplot2 y usando dplyr. La serie de tiempo las vas conectar con getSymbols para bajar un ticket de un activo financiero, en este caso el activo deberá ser de Apple Inc. El gráfico debe ser muy profesional, limpio y visualmente atractivo para usarse en análisis financiero.")

## Configurar chat al atajo (ctrl + g) ----

options(gander.chat = ellmer::chat_google_gemini(model = "gemini-3.6-flash"))

pacman::p_load(quantmod, tidyverse)

getSymbols("AAPL", src = "yahoo", auto.assign = TRUE)

ggplot(aapl_df, aes(x = Date, y = AAPL.Adjusted)) +
  geom_area(fill = "#003366", alpha = 0.1) +
  geom_line(color = "#003366", linewidth = 0.8) +
  scale_y_continuous(labels = scales::dollar_format()) +
  scale_x_date(date_labels = "%b %Y") +
  labs(
    title = "Apple Inc. (AAPL) - Precio de Cierre Ajustado",
    subtitle = "Evolución histórica del activo financiero",
    x = NULL,
    y = "Precio (USD)",
    caption = "Fuente: Yahoo Finance"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14, color = "#111111"),
    plot.subtitle = element_text(color = "#555555", size = 10, margin = margin(b = 10)),
    panel.grid.minor = element_blank(),
    axis.title.y = element_text(size = 10, color = "#333333"),
    axis.text = element_text(color = "#444444")
  )

aapl_df <- AAPL %>%
  as.data.frame() %>%
  rownames_to_column(var = "Date") %>%
  as_tibble() %>%
  mutate(Date = as.Date(Date))

aapl_df %>%
  mutate(
    SMA50 = TTR::SMA(AAPL.Adjusted, n = 50),
    SMA200 = TTR::SMA(AAPL.Adjusted, n = 200)
  ) %>%
  pivot_longer(
    cols = c(AAPL.Adjusted, SMA50, SMA200),
    names_to = "Indicator",
    values_to = "Price"
  ) %>%
  mutate(
    Indicator = factor(
      Indicator,
      levels = c("AAPL.Adjusted", "SMA50", "SMA200"),
      labels = c("Precio Ajustado", "Media Móvil (50d)", "Media Móvil (200d)")
    )
  ) %>%
  ggplot(aes(x = Date, y = Price, color = Indicator, linewidth = Indicator)) +
  geom_line(na.rm = TRUE) +
  scale_color_manual(
    values = c(
      "Precio Ajustado" = "#111827",
      "Media Móvil (50d)" = "#2563EB",
      "Media Móvil (200d)" = "#DC2626"
    )
  ) +
  scale_linewidth_manual(
    values = c(
      "Precio Ajustado" = 0.5,
      "Media Móvil (50d)" = 0.9,
      "Media Móvil (200d)" = 0.9
    )
  ) +
  scale_y_continuous(labels = scales::dollar_format(), position = "right") +
  scale_x_date(date_breaks = "2 years", date_labels = "%Y") +
  labs(
    title = "Apple Inc. (AAPL) - Análisis de Tendencia Técnica",
    subtitle = "Evolución del precio de cierre ajustado e indicadores de medias móviles",
    x = NULL,
    y = "Precio (USD)",
    color = NULL,
    linewidth = NULL,
    caption = "Fuente: Yahoo Finance via quantmod"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 15, color = "#0F172A"),
    plot.subtitle = element_text(color = "#475569", size = 10, margin = margin(b = 12)),
    legend.position = "top",
    legend.justification = "left",
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(color = "#F1F5F9"),
    axis.title.y.right = element_text(size = 9, color = "#334155", margin = margin(l = 8)),
    axis.text = element_text(color = "#64748B", size = 9),
    plot.caption = element_text(color = "#94A3B8", size = 8, margin = margin(t = 12))
  )


# Groq ----

## API de Groq ----

API_groq <-  "APIKEY"
Sys.setenv(GROQ_API_KEY = API_groq)

## Modelos de Groq ----

models_groq(
  api_key = API_groq
)

## Especificación del chat -----

chat_GROQ <- chat_groq(model = "qwen/qwen3.8-27b")

## Chat en vivo mediante consola ----

live_console(chat_GROQ)

# Prompt: Realiza código de R para estimar y validar una regresión lineal múltiple. Como datos utiliza la información de mtcars que viene disponible. La variable dependiente es mpg, las independientes son cyl, disp y wt. Valida los supuestos de la RLM (multicolinealidad, homocedasticidad, correlación serial, normalidad de residuos). Implementa gráficos con ggplot2 y dplyr a un nivel visual alto, es para presentación académica y como refuerzo al análisis del modelo.

## Enviar prompts al chat directo y la respuesta en consola ----

chat_GROQ$chat("Realiza código de R para estimar y validar una regresión lineal múltiple. Como datos utiliza la información de mtcars que viene disponible. La variable dependiente es mpg, las independientes son cyl, disp y wt. Valida los supuestos de la RLM (multicolinealidad, homocedasticidad, correlación serial, normalidad de residuos). Implementa gráficos con ggplot2 y dplyr a un nivel visual alto, es para presentación académica y como refuerzo al análisis del modelo.")

## Configurar chat al atajo (ctrl + g) ----

options(gander.chat = ellmer::chat_groq(model = "qwen/qwen3.8-27b"))

pacman::p_load(quantmod, tidyverse, TTR, scales)

if (!exists("AAPL")) {
  getSymbols("AAPL", src = "yahoo", auto.assign = TRUE)
}

aapl <- AAPL %>%
  as.data.frame() %>%
  rownames_to_column(var = "Date") %>%
  as_tibble() %>%
  mutate(
    Date = as.Date(Date),
    Close = AAPL.Close,
    MA20  = TTR::SMA(Close, n = 20),
    MA50  = TTR::SMA(Close, n = 50),
    MA200 = TTR::SMA(Close, n = 200)
  )


aapl_long <- aapl %>%
  select(Date, Close, MA20, MA50, MA200) %>%
  pivot_longer(
    cols = c(Close, MA20, MA50, MA200),
    names_to  = "series",
    values_to = "price"
  ) %>%
  mutate(
    series = factor(
      series,
      levels = c("Close", "MA20", "MA50", "MA200"),
      labels = c("Precio", "MM 20 días", "MM 50 días", "MM 200 días")
    )
  )

p <- ggplot(aapl_long, aes(x = Date, y = price, color = series)) +
  geom_line(na.rm = TRUE, linewidth = 0.9) +
  geom_area(
    data = filter(aapl_long, series == "Precio"),
    aes(x = Date, y = price),
    fill = "#1E88E5",
    alpha = 0.2,
    inherit.aes = FALSE,
  ) +
  scale_color_manual(
    values = c(
      "Precio"          = "#1E88E5",
      "MM 20 días"      = "#F57C00",
      "MM 50 días"      = "#8E24AA",
      "MM 200 días"     = "#D32F2F"
    )
  ) +
  scale_linewidth_manual(values = 0.9) +
  scale_y_continuous(labels = dollar_format(accuracy = 1)) +
  scale_x_date(date_breaks = "1 year", date_labels = "%b %Y") +
  labs(
    title    = "Apple Inc. (AAPL) — Tendencia de Precio y Medias Móviles",
    subtitle = "Gráfico profesional para análisis financiero técnico",
    x        = NULL,
    y        = "Precio (USD)",
    color    = NULL,
    caption  = "Fuente: Yahoo Finance vía quantmod"
  ) +
  theme_minimal(base_size = 11) +
  theme(
    plot.title      = element_text(face = "bold", size = 15, color = "#111111", hjust = 0.5),
    plot.subtitle   = element_text(size = 11, color = "#555555", hjust = 0.5, margin = margin(b = 12)),
    plot.caption    = element_text(size = 9, color = "#999999", hjust = 1),
    panel.background  = element_rect(fill = "white", color = NA),
    panel.grid.minor  = element_blank(),
    panel.grid.major  = element_line(color = "#EEEEEE", linewidth = 0.3),
    legend.position   = "top",
    legend.background = element_blank(),
    legend.justification = "center",
    legend.text     = element_text(size = 9, color = "#444444"),
    axis.title.y    = element_text(size = 10, color = "#333333", margin = margin(r = 10)),
    axis.title.x    = element_text(size = 9, color = "#666666"),
    axis.text.y     = element_text(size = 9, color = "#444444"),
    axis.text.x     = element_text(size = 9, color = "#444444"),
    axis.line       = element_line(color = "#CCCCCC", linewidth = 0.4)
  )

plot(p)


# Openrouter ----

## APIS ----

API_OR <- "APIKEY"
Sys.setenv(OPENROUTER_API_KEY = API_OR)

## Especificaciones del chat ----

chat_OR <- chat_openrouter(
  system_prompt = "Eres un experto en programación con R, responde con coherencia y lógica programativa",
  model = "nvidia/nemotron-3-ultra-550b-a55b:free"
)

## Live chat 

live_console(chat_OR)

options(gander.chat = ellmer::chat_openrouter(
  system_prompt = "Eres un experto en programación con R, responde con coherencia y lógica programativa",
  model = "nvidia/nemotron-3-ultra-550b-a55b:free"
))

