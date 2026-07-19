# Lecture Builder 3.0

Lecture Builder — многоагентная система подготовки русскоязычных лекций вузовского уровня. Версия 3.0 использует единое платформонезависимое ядро для Antigravity, Codex и совместимого режима Gemini, а качество результата контролируется не только промптами, но и JSON Schema, evidence ledger, хеш-манифестом, Python-валидаторами и DOCX smoke-тестами.

## Что изменилось в версии 3.0

- Канонические правила, workflows и Skills перенесены в `.agents/`.
- Antigravity использует `.agents/rules/`, `.agents/workflows/` и `.agents/skills/` напрямую.
- Codex использует настоящие TOML-профили в `.codex/agents/`, а не Markdown-обёртки над Gemini.
- Gemini сохранён как compatibility adapter; научная методология больше не дублируется в `.gemini/`.
- Поиск охватывает каждый вопрос лекции, а лимиты задаются конфигурацией.
- Источники, фрагменты, тезисы и ссылки связаны через `evidence_ledger.json`.
- Неизвестные авторы, годы, DOI и страницы не восстанавливаются «по смыслу».
- Перед написанием разделов создаётся общий `lecture_blueprint` с графом понятий и логическими связками.
- Формулы получают стабильные метки при написании и сквозные номера только после сборки всей лекции.
- Научная и педагогическая рецензии выполняются независимо; после редактирования проводится отдельный fact check.
- DOCX проверяется на нативные OMML-формулы, номера справа, поля, шрифт и колонтитул.
- Возобновление работы опирается на хеши входов и выходов, а не на наличие файлов.

## Архитектура

```text
config
  → literature search
  → source extraction
  → evidence curation
  → lecture architecture
  → section writers × N
  → coherence assembly
  → scientific review ┐
  → pedagogical review ┘
  → final editing
  → independent fact check
  → lecture-wide formula numbering
  → illustration planning
  → DOCX publishing
  → strict quality gate
```

Основные каталоги:

```text
.agents/rules/       постоянные инварианты проекта
.agents/workflows/   команды полного и частичного pipeline
.agents/skills/      общие знания и методы для всех платформ
.codex/agents/       Codex custom agents в TOML
.gemini/             compatibility adapter
contracts/           JSON Schema всех машинных артефактов
lecture_tools/       детерминированные проверки
scripts/             CLI, нумерация формул и DOCX
input/               пользовательская конфигурация и литература
output/              генерируемые материалы
```

Подробная схема приведена в `docs/ARCHITECTURE.md`.

## Быстрый старт

### 1. Установка проверок

```bash
git clone https://github.com/f2re/lecture-builder.git
cd lecture-builder
python -m pip install -e '.[dev]'
python scripts/validate_pipeline.py --mode source
pytest
```

Для DOCX требуется Pandoc. Обёртка `scripts/md2docx/run_md2docx.sh` создаёт локальное virtual environment для Python-зависимостей.

### 2. Конфигурация

Заполните `input/lecture_config.md`. Обязательные поля включают отдельный `lecture_number`, чтобы номер лекции не извлекался из произвольной строки `course`.

```yaml
lecture_number: 4
topic: "Основы абсолютной и относительной барической топографии"
discipline: "Синоптическая метеорология"
specialty: "05.03.04 Гидрометеорология"
course: "3 курс, 6 семестр"
hours: 2
fgos_version: "ФГОС 3++"
competencies:
  - "ОПК-1: ..."
audience_level: "бакалавры 3 курса"
questions:
  - "1. Физические основы абсолютной барической топографии"
language: ru
formulas_required: true
```

Полный шаблон: `input/lecture_config.example.md`.

### 3. Запуск в Antigravity

Используйте workspace workflow:

```text
/build-lecture
```

Доступны также:

```text
/research-literature
/design-lecture
/write-section
/review-lecture
/publish-docx
/resume-lecture
```

### 4. Запуск в Codex

Откройте репозиторий в Codex. Корневой `AGENTS.md` задаёт проектную политику, `.codex/config.toml` ограничивает безопасный параллелизм, а профили `.codex/agents/*.toml` делят роли. Для полного запуска поручите `lecture_orchestrator` выполнить workflow `.agents/workflows/build-lecture.md`.

### 5. Совместимый запуск Gemini

Старые команды сохранены как адаптеры:

```bash
gemini build-lecture
gemini search-literature
gemini write-section 2
gemini review-lecture
```

Они должны следовать каноническим Skills из `.agents/`; `.gemini` больше не является источником научных правил.

## Научная прослеживаемость

Каноническая ссылка внутри Markdown:

```text
[@src_001]
[@src_001, с. 45]
```

Страница допустима только при `location_status: verified`. Каждый научный тезис получает `claim_id`, отмечается в Markdown комментарием `<!-- claim:claim_id -->` и ссылается на один или несколько `evidence_id`, содержащих точный фрагмент, источник, хеш документа и координаты. Комментарии удаляются при DOCX-конвертации. Неподтверждённый тезис блокирует публикацию.

## Формулы

Во время написания используется семантическая метка:

```latex
$$
\Delta H = \frac{R\overline{T_v}}{g_0}\ln\frac{p_1}{p_2}
\label{eq:hypsometric}
$$
```

Ссылка в тексте: `@eq:hypsometric`. Финальные номера `(4.1)`, `(4.2)` назначаются один раз после сборки:

```bash
python scripts/number_formulas.py output/lecture_final.md \
  -o output/lecture_final.md \
  --registry output/formula_registry.json
```

## Проверки

```bash
# Исходная конфигурация, Skills, TOML и схемы
python scripts/validate_pipeline.py --mode source

# Модульные и интеграционные тесты
pytest

# Полный набор с обязательными артефактами
python scripts/validate_pipeline.py --mode artifacts --strict \
  --report output/quality_report.json

# DOCX
bash scripts/md2docx/run_md2docx.sh output/lecture_final.md \
  -o output/lecture_final.docx
python scripts/validate_docx.py output/lecture_final.docx --expect-formulas
```

Quality gate проверяет конфигурацию, схемы, ссылки, evidence ledger, формулы, структуру лекции, связность, рецензии, fact check, иллюстрации, manifest и DOCX. Критерии описаны в `docs/QUALITY_GATES.md`. Для взвешенного A/B-сравнения платформ используйте `python evals/run_evals.py`; три типовых конфигурации находятся в `evals/fixtures/`.

## Выходные материалы

Главные результаты:

- `output/lecture_final.md` — проверенный Markdown;
- `output/lecture_final.docx` — Word-документ с нативными формулами;
- `output/bibliography.json` — библиография с происхождением метаданных;
- `output/evidence_ledger.json` — связь тезисов и доказательств;
- `output/lecture_blueprint.json` — логическая архитектура;
- `output/reviews/` — независимые рецензии, resolution и fact check;
- `output/formula_registry.json` — сквозной реестр формул;
- `output/quality_report.json` — итог проверок;
- `output/run_manifest.json` — хеши и статус этапов.

## Миграция

Для безопасного обновления старой конфигурации без перезаписи исходника:

```bash
python scripts/migrate_v2.py input/lecture_config.md -o input/lecture_config.v3.md
```

Режим `--in-place` создаёт резервную копию `.v2.bak` и применяется только по явному запросу.

Существующие особенности Gemini-проекта сохранены: отдельные роли, один раздел на один запуск, локальная литература, промежуточные артефакты, ФГОС, ГОСТ-ориентированное оформление, иллюстрации и DOCX. Изменён источник истины и добавлены формальные гарантии. Подробности: `docs/MIGRATION_ANTIGRAVITY_CODEX.md`.
