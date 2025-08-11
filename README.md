# Pomodoro Hearts - Twilight Town

**Pomodoro Hearts** es una aplicación de temporizador Pomodoro desarrollada con Python y Tkinter. Utiliza una interfaz gráfica inspirada en "Twilight Town" (Kingdom Hearts), con música de fondo y funcionalidad completa para estudiar o trabajar de forma eficiente usando la técnica Pomodoro.

## Características

- Temporizador configurable basado en la técnica Pomodoro:
  - 20 minutos de trabajo
  - 5 minutos de descanso corto
  - 15 minutos de descanso largo cada 4 ciclos
- Interfaz gráfica responsiva (se ajusta al redimensionar la ventana)
- Fondo ilustrativo con música ambiental
- Botones de **Start**, **Pause** y **Reset**
- Código organizado y limpio, listo para ser extendido

## Requisitos

- Python 3.8 o superior
- Dependencias:
  - `pygame`
  - `Pillow`

Instalación de dependencias:

```bash
pip install pygame Pillow
```

## Estructura del Proyecto

```
pomodoro-hearts/
│
├── main.py
├── assets/
│   ├── music_twilighttown.mp3
│   └── bg_twilighttown.png
└── README.md
```

## Uso

1. Clona el repositorio:
   ```bash
   git clone https://github.com/egrazm/pomodoro-hearts.git
   cd pomodoro-hearts
   ```

2. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Empaquetado (opcional)

Puedes usar [PyInstaller](https://www.pyinstaller.org/) para generar un ejecutable:

```bash
pyinstaller --noconsole --onefile --add-data "assets;assets" main.py
```

Esto creará un ejecutable independiente en la carpeta `dist/`.
