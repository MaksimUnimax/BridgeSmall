# Acceptance test

## Server gate

Codex должен подтвердить:

```text
systemctl is-active business-bridge-2.service = active
GET /v2/health = 200
GET /v2/identity = 200
GET /v2/executors = 200
listener = 127.0.0.1:<port>
```

## Tunnel gate

На операторском компьютере:

```powershell
Invoke-RestMethod http://127.0.0.1:18083/v2/health
```

Ответ должен содержать:

```text
ok=true
api_contract=business-bridge-v2
server_version=2.0.0-alpha.2
```

## Extension gate

1. Профиль сохраняется.
2. Identity совпадает с отчётом Codex.
3. «Проверить соединение» показывает подключение.
4. Каталог CLI содержит хотя бы один enabled executor.
5. Диалог явно привязан.
6. Выбран executor следующей итерации.
7. Включён ручной режим writing blocks.

## End-to-end gate

ChatGPT создаёт один безопасный тестовый writing block с заданием CLI создать временный файл, прочитать его и удалить.

Оператор нажимает локальную Copy-кнопку блока один раз.

Успех:

- создан ровно один server job;
- CLI запускается ровно один раз;
- report доставляется ровно один раз;
- report появляется как новый user-turn ChatGPT;
- delivery переходит в confirmed;
- повторного Send нет;
- другой диалог не получает report;
- tunnel не открывает серверный port во внешний интернет.

## Безопасное тестовое задание

```text
Выполни проверку Business Bridge в текущей рабочей директории. Создай временный файл bb2_acceptance_probe.txt со строкой BB2_OK, прочитай и проверь содержимое, затем удали файл. Не изменяй другие файлы. В финальном отчёте укажи только: working_directory, create_ok, content_ok, delete_ok.
```
