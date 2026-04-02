#!/bin/bash
# run_md2docx.sh — Автоматический запуск конвертации с проверкой venv

# Сохраняем абсолютный путь к входному файлу
INPUT_FILE=$(realpath "$1")
shift

# Обработка аргументов для корректного разрешения путей
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE=$(realpath "$2")
            ARGS+=("-o" "$OUTPUT_FILE")
            shift 2
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done

# Переходим в директорию скрипта для работы с venv и reference.docx
cd "$(dirname "$0")"
VENV_PYTHON="./venv/bin/python3"

# Если venv нет или нет установленного пакета, запускаем установку
if [ ! -f "$VENV_PYTHON" ] || ! ./"$VENV_PYTHON" -c "import docx" &>/dev/null; then
    bash setup.sh
fi

# Запуск основного скрипта
./"$VENV_PYTHON" md2docx_gost.py "$INPUT_FILE" "${ARGS[@]}"
