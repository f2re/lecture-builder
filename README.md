# Lecture Builder 3.1

Lecture Builder — многоагентная система подготовки русскоязычных лекций вузовского уровня для Antigravity, Codex и совместимого режима Gemini. Канонические правила находятся в `.agents/`, а качество контролируют evidence ledger, локальная база источников, JSON Schema, детерминированная нумерация, независимые рецензии, fact check и DOCX-проверки.

## Что формирует система

Готовая лекция включает:

- логически связанную теорию и определения;
- формулы с расшифровкой символов, единицами и сквозной нумерацией;
- тематические примеры, мнемоники, предупреждения об ошибках и самопроверку;
- графики, схемы, карты и подписи, согласованные с источниками;
- отдельный `output/image_prompts.md` для генерации научных иллюстраций;
- `output/chart_specs.json` для детерминированных графиков без выдуманных данных;
- библиографию, evidence ledger и локальную базу литературы для сверки;
- независимую научную и педагогическую рецензию;
- финальный source-based fact check;
- Markdown и ГОСТ-ориентированный DOCX.

Система проверяет теорию по источникам и локальному корпусу, но не воспроизводит научные эксперименты: экспериментальная репликация не входит в задачу генерации лекции.

## Архитектура

```text
config
  → literature search + local source index
  → exact source extraction
  → bibliography + evidence ledger
  → numbered lecture blueprint + section briefs
  → section writers × N
  → deterministic structure numbering
  ├─→ methodical enhancer
  └─→ visualization planner
       → figures index + chart specs + separate image prompts
       → deterministic chart rendering
  → coherence assembly
  ├─→ scientific review
  └─→ pedagogical review
  → final editing
  → independent fact check
  → lecture-wide formula numbering
  → DOCX publishing
  → strict quality gate
```

Основные каталоги:

```text
.agents/rules/       постоянные инварианты
.agents/workflows/   команды Antigravity
.agents/skills/      общие Skills всех платформ
.codex/agents/       Codex custom agents в TOML
.gemini/             compatibility adapter
contracts/           JSON Schema
lecture_tools/       детерминированные проверки
scripts/             CLI и DOCX
input/               конфигурация и локальная литература
output/              генерируемые материалы
```

## Нумерация от номера лекции

`lecture_number` задаётся в `input/lecture_config.md`. Для лекции 17:

```yaml
lecture_number: 17
questions:
  - "17.1. Первый учебный вопрос"
  - "17.2. Второй учебный вопрос"
```

В готовом документе:

```text
Вопросы:      17.1, 17.2, 17.3
Подразделы:   17.1.1, 17.1.2; 17.2.1, 17.2.2
Формулы:      (17.1), (17.2), (17.3) — сквозной счётчик
Рисунки:      Рисунок 17.1, Рисунок 17.2 — сквозной счётчик
Таблицы:      Таблица 17.1, Таблица 17.2 — сквозной счётчик
```

Это отдельные пространства нумерации: номер `17.1` может одновременно обозначать первый вопрос, первую формулу и первый рисунок. Технические пути сохраняют локальный номер: `section_1_...`.

Нормализация и проверка:

```bash
python scripts/number_structure.py output/lecture_final.md -o output/lecture_final.md
python scripts/validate_numbering.py output/lecture_final.md
```

## Методические вставки

Новый `methodical-enhancer` анализирует все готовые разделы и создаёт `output/methodical_inserts.json`. Он не переписывает научный текст, а проектирует короткие вставки:

```markdown
> **Ключевая идея.** ...

> **Мнемоника.** ...

> **Тематический пример к вопросу 17.1.** ...

> **Как читать формулу.** ...

> **Типичная ошибка.** ...

> **Проверка понимания.** ...
```

Вставки распределяются по функциям `understand`, `remember`, `apply`, `self_check` и `transfer`, ограничиваются по плотности и проходят научную, педагогическую и финальную проверку. Фактические вставки связаны с claim/evidence; условные численные ситуации помечаются как иллюстративные.

## Графики и изображения

`visualization-planner` создаёт:

- `output/figures_index.json` — рисунки с номерами, подписями и alt text;
- `output/chart_specs.json` — оси, единицы, источники данных и преобразования для графиков;
- `output/image_prompts.md` — отдельные tool-neutral промпты для схем, карт и научных иллюстраций.

Наблюдательные кривые и карты нельзя поручать генеративной модели без данных. График либо строится детерминированно из cited/local dataset, либо явно отмечается как схематический и не являющийся наблюдательными данными. Построение выполняется командой:

```bash
python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json
```

Скрипт синхронизирует статусы и пути в обоих JSON-файлах, сохраняет asset/data hashes и создаёт PNG/SVG под `output/figures/`.

## Быстрый старт

```bash
git clone https://github.com/f2re/lecture-builder.git
cd lecture-builder
python -m pip install -e '.[dev]'
python scripts/validate_pipeline.py --mode source
pytest
```

Заполните `input/lecture_config.md`; полный шаблон находится в `input/lecture_config.example.md`.

### Antigravity

```text
/build-lecture
/research-literature
/design-lecture
/write-section
/enrich-lecture
/plan-visuals
/review-lecture
/publish-docx
/resume-lecture
```

### Codex

Поручите `lecture_orchestrator` выполнить `.agents/workflows/build-lecture.md`. Узкие профили находятся в `.codex/agents/`, включая `methodical_enhancer` и `visualization_planner`.

### Gemini compatibility

```bash
gemini build-lecture
gemini search-literature
gemini write-section 2
gemini enrich-lecture
gemini plan-visuals
gemini review-lecture
```

Gemini-адаптеры читают канонические Skills из `.agents/`.

## Научная прослеживаемость

Внутренняя ссылка:

```text
[@src_001]
[@src_001, с. 45]
```

Страница допустима только при `location_status: verified`. Каждый существенный тезис получает `claim_id` и точный evidence fragment. Локальные PDF/DOCX/тексты индексируются в `output/lit/local_index.json` и используются наравне с проверенными веб-источниками.

## Формулы

При написании используется стабильная метка:

```latex
$$
\Delta H = \frac{R\overline{T_v}}{g_0}\ln\frac{p_1}{p_2}
\label{eq:hypsometric}
$$
```

После fact check:

```bash
python scripts/number_formulas.py output/lecture_final.md \
  -o output/lecture_final.md \
  --registry output/formula_registry.json
```

## Проверки и публикация

```bash
python scripts/validate_pipeline.py --mode source
pytest
python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json
python scripts/validate_pipeline.py --mode artifacts --strict \
  --report output/quality_report.json
bash scripts/md2docx/run_md2docx.sh output/lecture_final.md \
  -o output/lecture_final.docx
python scripts/validate_docx.py output/lecture_final.docx --expect-formulas
```

Главные результаты: `lecture_final.md`, `lecture_final.docx`, `bibliography.json`, `evidence_ledger.json`, `lecture_blueprint.json`, `methodical_inserts.json`, `chart_specs.json`, `image_prompts.md`, `figures_index.json`, `reviews/`, `formula_registry.json`, `quality_report.json` и `run_manifest.json`.
