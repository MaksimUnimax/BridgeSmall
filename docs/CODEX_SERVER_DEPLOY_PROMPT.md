# Промпт для Codex на сервере

Скопируй весь текст ниже в Codex, запущенный на целевом сервере.

---

Ты разворачиваешь Business Bridge 2 из репозитория `MaksimUnimax/BridgeSmall`.

Цель: установить и проверить серверную часть, не меняя посторонние сервисы и не публикуя Bridge API в интернет.

Обязательный порядок:

1. Клонируй репозиторий или обнови уже существующую рабочую копию.
2. Прочитай полностью `README.md`, `AGENTS.md`, `server/README.md`, `docs/ACCEPTANCE_TEST.md` и `docs/TROUBLESHOOTING.md`.
3. Проверь, что система использует systemd и доступен Python 3.10+.
4. Определи публичный IP/hostname, SSH port и SSH user, через которые оператор подключается к серверу.
5. Проверь наличие хотя бы одной CLI: `codex`, `codex2`, `codex3` или `mimo`.
6. Проверь, свободен ли `127.0.0.1:18083`.
7. Если порт занят посторонним процессом или сервисом, ничего не останавливай. Заверши задачу с отчётом о конфликте.
8. Если `business-bridge-2.service` уже существует, ничего не обновляй без отдельного разрешения владельца.
9. Восстанови server package и проверь его SHA-256:

```bash
python3 tools/materialize.py --server
```

Materializer обязан подтвердить SHA-256 `000c3f87662e3037b6bfd45e00fbc25413b18a0093fe7bc25fb9631df6ae7cdb`.

10. На новом сервере выполни из корня репозитория:

```bash
sudo bash server/scripts/install.sh
```

11. Проверь:

```bash
sudo systemctl status business-bridge-2.service --no-pager
sudo python3 server/scripts/verify.py \
  --endpoint http://127.0.0.1:18083 \
  --token-file /opt/business-bridge-2/secrets/control_api.token
```

12. Убедись, что listener — только `127.0.0.1:18083`, а не `0.0.0.0`.
13. Не запускай пользовательскую CLI-задачу без отдельного запроса. Health, identity и executor catalog достаточно для deployment gate.
14. Верни оператору следующие проверенные значения:

```text
status=installed_and_verified
service=business-bridge-2.service
listener=127.0.0.1:18083
ssh_host=<PUBLIC_IP_OR_HOSTNAME>
ssh_port=<SSH_PORT>
ssh_user=<SSH_USER>
remote_bridge_port=18083
instance_id=<INSTANCE_UUID>
executor_ids=<COMMA_SEPARATED_IDS>
token=<BEARER_TOKEN>
health=200
identity=200
executors=200
rollback_backup=<PATH_OR_NONE>
```

Token передай только владельцу в этом приватном диалоге. Не записывай token в Git, issue, documentation, shell history или публичные логи.

Не изменяй Bridge 1. Не останавливай посторонние сервисы. Не открывай firewall port для Bridge 2. Доступ должен идти только через SSH local forwarding.

---
