# Business Bridge 2 server 2.0.0-alpha.2

## Требования

- Linux с systemd;
- root-доступ для compatibility deployment;
- Python 3.10 или новее;
- хотя бы один настроенный CLI: `codex`, `codex2`, `codex3` или `mimo`;
- свободный loopback port, по умолчанию `18083`;
- SSH-доступ к серверу.

Python-зависимостей из PyPI нет: реализация использует стандартную библиотеку.

## Восстановление server package

```bash
python3 tools/materialize.py --server
```

Ожидаемый SHA-256:

```text
000c3f87662e3037b6bfd45e00fbc25413b18a0093fe7bc25fb9631df6ae7cdb
```

## Установка

```bash
sudo bash server/scripts/install.sh
```

Переопределение параметров:

```bash
sudo \
  BB2_INSTALL_PORT=18083 \
  BB2_INSTALL_ROOT=/opt/business-bridge-2 \
  BB2_EXECUTOR_WORKDIR=/root \
  bash server/scripts/install.sh
```

## Проверка

```bash
sudo python3 server/scripts/verify.py \
  --endpoint http://127.0.0.1:18083 \
  --token-file /opt/business-bridge-2/secrets/control_api.token
```

## Runtime paths

```text
/opt/business-bridge-2/state/bridge.sqlite3
/opt/business-bridge-2/state/instance.json
/opt/business-bridge-2/secrets/control_api.token
/opt/business-bridge-2/artifacts/jobs/
```

Token и instance file создаются приложением атомарно. Token содержит 32 random bytes в URL-safe base64 и хранится с mode `0600`.

## Executor config

Установщик создаёт `/opt/business-bridge-2/config/executors.json` из executables, реально найденных на сервере. Снимок конфигурации исходного сервера хранится только как reference и не должен копироваться вслепую.

## Security boundary

Listener должен оставаться `127.0.0.1`. Подключение расширения выполняется через SSH local forwarding. Нельзя открывать port Bridge 2 во внешний интернет.
