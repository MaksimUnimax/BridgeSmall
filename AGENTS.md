# AGENTS.md — инструкция Codex

## Цель

Развернуть Business Bridge 2 на Linux-сервере так, чтобы Chrome-расширение подключалось к нему только через локальный SSH-туннель.

## Источник истины

Перед действиями прочитай в таком порядке:

1. `README.md`
2. `AGENTS.md`
3. `server/README.md`
4. `docs/CODEX_SERVER_DEPLOY_PROMPT.md`
5. `docs/ACCEPTANCE_TEST.md`
6. `docs/TROUBLESHOOTING.md`

## Запреты

- не меняй Bridge 1;
- не останавливай посторонние сервисы;
- при конфликте порта остановись и сообщи владельцу;
- не публикуй token;
- не открывай listener на `0.0.0.0`;
- не добавляй произвольные shell-команды в browser API;
- не меняй API contract `business-bridge-v2`;
- не исправляй исходник без отдельного задания;
- не называй установку успешной до прохождения `verify.py`.

## Новый сервер

Сначала восстанови проверенный server package из частей репозитория:

```bash
python3 tools/materialize.py --server
```

Затем из корня репозитория выполни:

```bash
sudo bash server/scripts/install.sh
```

Установщик:

- проверяет root, systemd и Python 3.10+;
- проверяет конфликт `127.0.0.1:18083`;
- обнаруживает реально установленные `codex`, `codex2`, `codex3` и `mimo`;
- создаёт server-specific `config/executors.json`;
- устанавливает код в `/opt/business-bridge-2`;
- создаёт token и instance identity при первом запуске;
- устанавливает `business-bridge-2.service`;
- проверяет `/v2/health`, `/v2/identity` и `/v2/executors`;
- выводит параметры, которые нужно вернуть оператору.

## Обновление существующего Bridge 2

Не запускай обновление автоматически. Сначала изучи текущую установку и сделай план rollback. Только после явного разрешения владельца:

```bash
sudo BB2_ALLOW_UPDATE=1 bash server/scripts/install.sh
```

Установщик создаст backup и выведет его путь.

## Обязательный финальный ответ оператору

Верни только проверенные значения:

```text
status=installed_and_verified
service=business-bridge-2.service
listener=127.0.0.1:<PORT>
ssh_host=<PUBLIC_IP_OR_HOSTNAME>
ssh_port=<SSH_PORT>
ssh_user=<SSH_USER>
remote_bridge_port=<PORT>
instance_id=<INSTANCE_UUID>
executor_ids=<COMMA_SEPARATED_IDS>
token=<BEARER_TOKEN>
health=200
identity=200
executors=200
rollback_backup=<PATH_OR_NONE>
```

Token является секретом. Не записывай его в репозиторий, issue, лог или публичный документ.
