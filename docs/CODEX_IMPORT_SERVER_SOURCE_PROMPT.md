# Codex: импорт очищенного серверного исходника в BridgeSmall

Передай этот файл Codex **на исходном сервере**, где существует каталог:

```text
/root/bridge-small-server-handoff-20260729-102000
```

Codex должен импортировать только очищенный handoff в GitHub, не изменяя установленный Business Bridge 2.

## Исполнительный промпт

Ты работаешь на сервере с уже подготовленным очищенным handoff Business Bridge 2:

```text
/root/bridge-small-server-handoff-20260729-102000
```

Целевой репозиторий:

```text
https://github.com/MaksimUnimax/BridgeSmall.git
```

Целевая ветка для изменений:

```text
codex/import-server-alpha2-20260729
```

### Цель

Импортировать в репозиторий полный очищенный серверный исходник, handoff-факты и воспроизводимые install/verify/rollback scripts. Не изменять установленный сервер.

### Жёсткие запреты

- Не редактировать `/opt/business-bridge-2`.
- Не останавливать, не перезапускать и не reload-ить сервисы.
- Не менять systemd, firewall, SSH, пакеты, executors, tokens, instance UUID или SQLite.
- Не копировать реальные секреты, БД, WAL/SHM, logs, artifacts, reports, backups, caches, `.git`, CLI credentials, SSH-материалы или Bridge 1.
- Не печатать GitHub token и не помещать его в commit, logs или shell history.
- Не делать force-push.
- Не пушить прямо в `main`.
- При отсутствии GitHub-аутентификации остановиться и вернуть точный безопасный способ выполнить `gh auth login`; не просить вставлять token в чат.

### 1. Проверка входного handoff

Проверь:

```bash
set -euo pipefail
HANDOFF=/root/bridge-small-server-handoff-20260729-102000
cd "$HANDOFF"
sha256sum SERVER_SOURCE_SANITIZED.tar.gz
```

Ожидаемый SHA-256:

```text
a84aaa9d98b9eaf706137813759d6d4a8430855894c7bcc017237837a7d925af
```

Проверь также:

```bash
sha256sum -c SHA256SUMS
```

При любом расхождении остановись без GitHub-записи.

### 2. Проверка GitHub-аутентификации

Сначала:

```bash
gh auth status
```

Если `gh` отсутствует, проверь SSH-аутентификацию без изменения сервера:

```bash
ssh -T git@github.com
```

Продолжай только если существующая аутентификация даёт право push в `MaksimUnimax/BridgeSmall`.

### 3. Безопасная рабочая копия

```bash
WORK=$(mktemp -d /root/bridge-small-github-import.XXXXXX)
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
git clone https://github.com/MaksimUnimax/BridgeSmall.git repo
cd repo
git checkout -b codex/import-server-alpha2-20260729 origin/main
```

Если используется SSH-auth, допускается clone через `git@github.com:MaksimUnimax/BridgeSmall.git`.

### 4. Распаковка и проверка allowlist

```bash
mkdir extracted
tar -xzf "$HANDOFF/SERVER_SOURCE_SANITIZED.tar.gz" -C extracted
```

Архив обязан иметь ровно один top-level каталог:

```text
SERVER_SOURCE_SANITIZED/
```

Проверь отсутствие symlinks, hardlinks, device files, FIFOs и absolute/parent-traversal paths. Сверь дерево с:

```text
$HANDOFF/SOURCE_TREE.txt
$HANDOFF/SERVER_SOURCE_FILE_SHA256SUMS.txt
$HANDOFF/VALIDATION_REPORT.md
```

### 5. Импорт в репозиторий

Создай или полностью замени только эти каталоги:

```text
server/source/
server/handoff/
server/scripts/
server/templates/
```

Содержимое:

- `server/source/` — точное содержимое `SERVER_SOURCE_SANITIZED/`, без изменения source-файлов;
- `server/handoff/` — копии:
  - `SERVER_INSTALL_FACTS.md`
  - `SYSTEMD_UNIT_SANITIZED.service`
  - `CONFIG_TEMPLATE.env.example`
  - `SOURCE_TREE.txt`
  - `SERVER_SOURCE_FILE_SHA256SUMS.txt`
  - `VALIDATION_REPORT.md`
  - `TEST_SOURCE_TESTS_OUTPUT.txt`
  - `SHA256SUMS`
- `server/templates/` — безопасные install templates, выведенные только из фактического sanitized unit/config;
- `server/scripts/` — воспроизводимые scripts, описанные ниже.

Не копируй сам `SERVER_SOURCE_SANITIZED.tar.gz` в Git: исходники должны находиться в обычном читаемом дереве.

### 6. Создай воспроизводимые scripts

На основании фактических файлов handoff и source создай:

```text
server/scripts/install.sh
server/scripts/verify.py
server/scripts/rollback.sh
```

`install.sh` обязан:

- работать на Linux с systemd;
- по умолчанию устанавливать в `/opt/business-bridge-2`;
- по умолчанию использовать listener `127.0.0.1:18083` и API prefix `/v2`;
- до изменений проверять свободный port;
- при конфликте port останавливаться и ничего не останавливать автоматически;
- создавать backup только существующего Bridge 2;
- не трогать Bridge 1 и посторонние services;
- генерировать новый случайный token не короче 32 bytes;
- генерировать новый instance UUID;
- хранить secret files с mode `0600`;
- создавать executor config только из executables, реально найденных на целевом сервере;
- не принимать arbitrary shell commands от browser/API;
- устанавливать exact sanitized systemd unit с параметризованными безопасными путями;
- выполнять daemon-reload, enable и start только после всех preflight checks;
- при failed verification автоматически останавливать только новый Bridge 2 и восстанавливать его backup;
- печатать token только один раз оператору в terminal и никогда не писать его в Git/log/report.

`verify.py` обязан проверять:

- service active;
- listener только loopback;
- `GET /v2/health` = 200;
- authenticated `GET /v2/identity` = 200;
- authenticated `GET /v2/executors` = 200;
- API contract `business-bridge-v2`;
- server instance identity;
- SQLite integrity без вывода пользовательских данных;
- отсутствие секретов в structured logs.

`rollback.sh` обязан:

- затрагивать только `business-bridge-2.service` и `/opt/business-bridge-2`;
- не использовать Bridge 1 как rollback target;
- требовать явный путь backup;
- проверять backup до замены;
- сохранять failed deployment отдельно.

### 7. Документация

Обнови `server/README.md` так, чтобы она ссылалась на обычное дерево `server/source/`, а не на незавершённые Base64 server chunks.

Обнови корневой `README.md` только там, где нужно указать:

- серверный source находится в `server/source/`;
- Codex deploy prompt: `docs/CODEX_SERVER_DEPLOY_PROMPT.md`;
- ChatGPT/operator guide: `docs/CHATGPT_OPERATOR_GUIDE.md`;
- Chrome extension materialization остаётся отдельной операцией.

Не меняй документированный факт: кнопка `▶ Авторежим` скрыта только в UI; функциональность авторежима не удалена.

### 8. Тесты и secret scan

Запусти существующие server tests из disposable copy без установки новых зависимостей. Ожидаемый исходный handoff-результат:

```text
46 passed
10 subtests passed
```

Запусти shell syntax checks и Python compile checks для новых scripts.

Просканируй все staged files минимум на:

```text
Authorization: Bearer
BEGIN OPENSSH PRIVATE KEY
BEGIN RSA PRIVATE KEY
BEGIN PRIVATE KEY
password
passwd
cookie
session
api_key
secret
*.db
*.sqlite*
*-wal
*-shm
```

Совпадения в документационных placeholders разрешены только после ручной проверки. Реальные секреты запрещены.

### 9. Commit, push и PR

```bash
git status --short
git add server README.md AGENTS.md docs tools .github 2>/dev/null || true
git diff --cached --check
git commit -m "Import sanitized Business Bridge 2 server source"
git push -u origin codex/import-server-alpha2-20260729
```

Создай PR:

```bash
gh pr create \
  --repo MaksimUnimax/BridgeSmall \
  --base main \
  --head codex/import-server-alpha2-20260729 \
  --title "Import sanitized Business Bridge 2 server source" \
  --body "Imports the verified sanitized Business Bridge 2 alpha.2 source, reproducible deployment scripts, handoff facts, tests, and rollback instructions. No installed service or source file was modified."
```

Не merge-ить PR самостоятельно.

### 10. Финальный отчёт

Верни:

1. branch name;
2. commit SHA;
3. PR URL/number;
4. список добавленных файлов;
5. результат source tests;
6. результат syntax checks;
7. результат secret scan;
8. подтверждение отсутствия binary/runtime/secrets;
9. все отклонения от handoff;
10. подтверждение, изменялся ли установленный сервер.

Если это правда, закончи точной строкой:

```text
No installed service or source file was modified
```
