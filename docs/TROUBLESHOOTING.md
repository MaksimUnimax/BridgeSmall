# Диагностика

## `Invoke-RestMethod` не подключается

- SSH-туннель не запущен или завершился.
- Неверны SSH host/user/port.
- Local port занят.
- Server service не active.

Проверить:

```powershell
Test-NetConnection 127.0.0.1 -Port 18083
```

## Профиль не сохраняется

- endpoint должен быть `http://127.0.0.1:<local-port>` или localhost;
- token пустой или неверный;
- туннель не работает;
- endpoint отвечает другим `bridge_instance_id`.

## Каталог CLI пуст или executor unavailable

На сервере Codex должен проверить:

```bash
sudo cat /opt/business-bridge-2/config/executors.json
sudo python3 server/scripts/verify.py --endpoint http://127.0.0.1:18083 --token-file /opt/business-bridge-2/secrets/control_api.token
```

`static available` доказывает только наличие executable и working directory. Оно не доказывает provider authentication или доступный quota.

## Локальная Copy-кнопка не стала активной

- убедиться, что включён «Ручной режим writing blocks»;
- использовать Copy внутри code block, не общую «Копировать ответ»;
- обновить вкладку ChatGPT;
- при изменении DOM использовать «Выбрать Copy-кнопку» в popup.

## Report не отправляется

- проверить tunnel;
- открыть диагностику расширения;
- проверить, не требуется ли ручной выбор Send-кнопки;
- не нажимать Send повторно для delivery, которая могла пересечь commit boundary.

## Port 18083 занят на сервере

Не останавливать найденный сервис автоматически. Выбрать другой server port только после решения владельца и затем использовать его в `BB2_INSTALL_PORT` и SSH remote forward.

## Rollback после разрешённого update

```bash
sudo bash server/scripts/rollback.sh /root/business-bridge-2-before-YYYYMMDD-HHMMSS.tar.gz
```

Rollback затрагивает только Bridge 2.
