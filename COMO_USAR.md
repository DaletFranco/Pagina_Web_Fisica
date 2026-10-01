# 🚀 Guía de Uso: Visualizador Web de Flujos y PINNs

Esta guía explica cómo ejecutar, visualizar y trabajar con el proyecto de **Mecánica de Fluidos y Redes Neuronales Informadas por la Física (PINNs)**.

---

## 💻 1. ¿Cómo Abrir y Usar el Visualizador Web?

Para ver todos los gráficos y animaciones de forma limpia, ordenada y **sin sobrecargar la memoria RAM**:

### Opción A: Mediante el Servidor Web (Recomendado)
Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
python serve.py
```

- Este comando verificará los activos gráficos y levantará un servidor local rápido y liviano.
- Abrirá automáticamente tu navegador en:  
  👉 **[http://localhost:8000/web/index.html](http://localhost:8000/web/index.html)**

### Opción B: Apertura Directa en el Navegador
También puedes abrir el archivo `web/index.html` haciendo doble clic sobre él desde el explorador de archivos de Windows.

---

## 🎨 2. Funcionalidades de la Interfaz Web

- **Pestañas de Navegación**: Cambia cómodamente entre las distintas secciones del trabajo práctico:
  - **Problema 1: Flujos Adimensionales**:
    - *Inciso (i)*: Fuente + Corriente Creciente ($U(t')=t'$).
    - *Inciso (ii)*: Fuente + Torbellino Decayente ($\Gamma(t) = \Gamma_0 e^{-t/\tau}$).
    - *Inciso (iii)*: Fuente + Corriente Oscilante ($U(t') = \cos(\Omega t')$).
  - **Problema 2: Integración con PINNs**:
    - Solución RK4 de Referencia.
    - Convergencia del Entrenamiento Base ($N_d=10, N_f=20, \lambda=10^{-4}$).
    - Extrapolación ($t > T$) y Extensión a $[0, 2T]$.
    - Sensibilidad e Hiperparámetros (Barridos de $N_d$, $N_f$, $\lambda$).
    - Comparación de Arquitecturas Neuronales.
  - **Problema 3: Vórtice de Burgers (PIV)**:
    - Ajuste de trayectorias experimentales y estimación de parámetros físicos $(\alpha, \Gamma, r_0^2)$.
  - **Correcciones & Documentación**:
    - Detalle de los errores corregidos en docstrings y optimización de memoria.
- **Visor Modal en Alta Resolución**: Haz clic sobre cualquier gráfico para ampliarlo a pantalla completa.
- **Fórmulas Matemáticas**: Renderizado automático en LaTeX con MathJax.

---

## ⚙️ 3. Ejecución del Código de Cálculo en Python

Si deseas volver a ejecutar las simulaciones numéricas de Python o modificar el código base:

```bash
python g1_dacruz_jeifetz_teira.py
```

### Re-generar los Activos Gráficos Web
Si modificas los parámetros físicos y deseas actualizar las imágenes y animaciones de la página web, ejecuta:

```bash
python export_assets.py
```
*(O ejecuta `python serve.py --regenerate`)*

---

## 📂 4. Estructura de Archivos del Proyecto

```text
tp gio/
├── g1_dacruz_jeifetz_teira.py  # Script de Python corregido y optimizado
├── G1_DaCruz_Jeifetz_Teira.ipynb # Notebook original de Jupyter / Colab
├── serve.py                    # Servidor web local liviano (Lanza la web)
├── export_assets.py            # Generador de gráficos PNG y GIFs animados
├── README.md                   # Guía de uso del proyecto
├── COMO_USAR.md                # Guía de uso en español (este archivo)
└── web/
    ├── index.html              # Estructura principal de la interfaz web
    ├── style.css               # Estilos modernos Dark Mode & Glassmorphism
    ├── app.js                  # Lógica de pestañas, modales y renderizado
    └── assets/                 # Gráficos PNG y animaciones GIF comprimidas
```

---

## 🔧 5. Correcciones Aplicadas en el Código

1. **Notación Raw en Docstrings (`r"""..."""`)**: Corregidas todas las cadenas con barras invertidas `\` para evitar que Python reemplace secuencias como `\beta`, `\tau`, `\theta`, `\frac`, `\alpha` por caracteres de escape corruptos.
2. **Reparación de Markdown Corrupto**: Sustituidos artefactos como `1/r*2*` $\to$ `$1/r^2$` y `r*2*-->max(r*2,ϵ)` $\to$ `$r^2 \to \max(r^2, \epsilon)$`.
3. **Control de Memoria RAM**: Eliminado el almacenamiento simultáneo de cientos de figuras en RAM invocando `plt.close(fig)` inmediatamente después de cada renderizado.
